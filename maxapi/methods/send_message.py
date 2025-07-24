

import asyncio
from typing import Any, Dict, List, TYPE_CHECKING, Optional

from json import loads as json_loads

from ..utils.message import process_input_media

from ..exceptions.max import MaxUploadFileFailed

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
        attachments (List[Attachment | InputMedia | InputMediaBuffer], optional): Список вложений к сообщению.
        link (NewMessageLink, optional): Связь с другим сообщением (например, ответ или пересылка).
        notify (bool, optional): Отправлять ли уведомление о сообщении. По умолчанию True.
        parse_mode (ParseMode, optional): Режим разбора текста (например, Markdown, HTML).
    """
    
    def __init__(
            self,
            bot: 'Bot',
            chat_id: Optional[int] = None, 
            user_id: Optional[int] = None, 
            text: Optional[str] = None,
            attachments: Optional[List[Attachment | InputMedia | InputMediaBuffer]] = None,
            link: Optional[NewMessageLink] = None,
            notify: Optional[bool] = None,
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

    async def fetch(self) -> Optional[SendedMessage | Error]:
        
        """
        Отправляет сообщение с вложениями (если есть), с обработкой задержки готовности вложений.

        Возвращает результат отправки или ошибку.

        Возвращаемое значение:
            SendedMessage или Error
        """
        
        assert self.bot is not None
        params = self.bot.params.copy()

        json: Dict[str, Any] = {'attachments': []}

        if self.chat_id: params['chat_id'] = self.chat_id
        elif self.user_id: params['user_id'] = self.user_id

        json['text'] = self.text
        
        if self.attachments:
            
            for att in self.attachments:

                if isinstance(att, InputMedia) or isinstance(att, InputMediaBuffer):
                    input_media = await process_input_media(
                        base_connection=self,
                        bot=self.bot,
                        att=att
                    )
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