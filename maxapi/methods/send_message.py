

import asyncio
from typing import List, TYPE_CHECKING, Optional

from json import loads as json_loads

from .types.sended_message import SendedMessage
from ..types.attachments.upload import AttachmentPayload, AttachmentUpload
from ..types.errors import Error
from ..types.message import NewMessageLink
from ..types.input_media import InputMedia, InputMediaBuffer
from ..types.attachments.attachment import Attachment

from ..enums.upload_type import UploadType
from ..enums.parse_mode import ParseMode
from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath
from ..connection.base import BaseConnection

from ..loggers import logger_bot


if TYPE_CHECKING:
    from ..bot import Bot
    

RETRY_DELAY = 2
ATTEMPTS_COUNT = 5


class SendMessage(BaseConnection):
    
    """
    Класс для отправки сообщения в чат или пользователю с поддержкой вложений и форматирования.

    Args:
        bot (Bot): Экземпляр бота для выполнения запроса.
        chat_id (int, optional): Идентификатор чата, куда отправлять сообщение.
        user_id (int, optional): Идентификатор пользователя, если нужно отправить личное сообщение.
        text (str, optional): Текст сообщения.
        attachments (List[Attachment | InputMedia], optional): Список вложений к сообщению.
        link (NewMessageLink, optional): Связь с другим сообщением (например, ответ или пересылка).
        notify (bool, optional): Отправлять ли уведомление о сообщении. По умолчанию True.
        parse_mode (ParseMode, optional): Режим разбора текста (например, Markdown, HTML).
    """
    
    def __init__(
            self,
            bot: 'Bot',
            chat_id: int = None, 
            user_id: int = None, 
            text: str = None,
            attachments: List[Attachment | InputMedia] = None,
            link: NewMessageLink = None,
            notify: bool = True,
            parse_mode: Optional[ParseMode] = None
        ):
            self.bot = bot
            self.chat_id = chat_id
            self.user_id = user_id
            self.text = text
            self.attachments = attachments
            self.link = link
            self.notify = notify
            self.parse_mode = parse_mode

    async def __process_input_media(
            self,
            att: InputMedia | InputMediaBuffer
        ):
        
        # очень нестабильный метод независящий от модуля
        # ждем обновлений MAX API
        
        """
        Загружает файл вложения и формирует объект AttachmentUpload.

        Args:
            att (InputMedia): Объект вложения для загрузки.

        Returns:
            AttachmentUpload: Загруженное вложение с токеном.
        """
        
        upload = await self.bot.get_upload_url(att.type)

        if isinstance(att, InputMedia):
            upload_file_response = await self.upload_file(
                url=upload.url,
                path=att.path,
                type=att.type,
            )
        elif isinstance(att, InputMediaBuffer):
            upload_file_response = await self.upload_file_buffer(
                url=upload.url,
                buffer=att.buffer,
                type=att.type,
            )

        if att.type in (UploadType.VIDEO, UploadType.AUDIO):
            token = upload.token

        elif att.type == UploadType.FILE:
            json_r = json_loads(upload_file_response)
            token = json_r['token']
            
        elif att.type == UploadType.IMAGE:
            json_r = json_loads(upload_file_response)
            json_r_keys = list(json_r['photos'].keys())
            token = json_r['photos'][json_r_keys[0]]['token']
        
        return AttachmentUpload(
            type=att.type,
            payload=AttachmentPayload(
                token=token
            )
        )

    async def request(self) -> SendedMessage:
        
        """
        Отправляет сообщение с вложениями (если есть), с обработкой задержки готовности вложений.

        Возвращает результат отправки или ошибку.

        Возвращаемое значение:
            SendedMessage или Error
        """
        
        params = self.bot.params.copy()

        json = {'attachments': []}

        if self.chat_id: params['chat_id'] = self.chat_id
        elif self.user_id: params['user_id'] = self.user_id

        json['text'] = self.text
        
        if self.attachments:
            
            for att in self.attachments:

                if isinstance(att, InputMedia) or isinstance(att, InputMediaBuffer):
                    input_media = await self.__process_input_media(att)
                    json['attachments'].append(
                        input_media.model_dump()
                    ) 
                else:
                    json['attachments'].append(att.model_dump()) 
        
        if not self.link is None: json['link'] = self.link.model_dump()
        json['notify'] = self.notify
        if not self.parse_mode is None: json['format'] = self.parse_mode.value

        response = None
        for attempt in range(ATTEMPTS_COUNT):
            response = await super().request(
                method=HTTPMethod.POST, 
                path=ApiPath.MESSAGES,
                model=SendedMessage,
                params=params,
                json=json
            )

            if isinstance(response, Error):
                if response.raw.get('code') == 'attachment.not.ready':
                    logger_bot.info(f'Ошибка при отправке загруженного медиа, попытка {attempt+1}, жду {RETRY_DELAY} секунды')
                    await asyncio.sleep(RETRY_DELAY)
                    continue
            
            return response
        return response