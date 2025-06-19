

import asyncio
from typing import List, TYPE_CHECKING

from json import loads as json_loads

from ..enums.upload_type import UploadType

from ..types.attachments.upload import AttachmentPayload, AttachmentUpload
from ..types.errors import Error
from .types.sended_message import SendedMessage
from ..types.message import NewMessageLink
from ..types.input_media import InputMedia
from ..types.attachments.attachment import Attachment
from ..enums.parse_mode import ParseMode
from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath
from ..connection.base import BaseConnection
from ..loggers import logger_bot


if TYPE_CHECKING:
    from ..bot import Bot


class UploadResponse:
    token: str = None


class SendMessage(BaseConnection):
    def __init__(
            self,
            bot: 'Bot',
            chat_id: int = None, 
            user_id: int = None, 
            disable_link_preview: bool = False,
            text: str = None,
            attachments: List[Attachment | InputMedia] = None,
            link: NewMessageLink = None,
            notify: bool = True,
            parse_mode: ParseMode = None
        ):
            self.bot = bot
            self.chat_id = chat_id
            self.user_id = user_id
            self.disable_link_preview = disable_link_preview
            self.text = text
            self.attachments = attachments
            self.link = link
            self.notify = notify
            self.parse_mode = parse_mode

    async def __process_input_media(
            self,
            att: InputMedia
        ):
        upload = await self.bot.get_upload_url(att.type)

        upload_file_response = await self.upload_file(
            url=upload.url,
            path=att.path,
            type=att.type
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
        params = self.bot.params.copy()

        json = {'attachments': []}

        if self.chat_id: params['chat_id'] = self.chat_id
        elif self.user_id: params['user_id'] = self.user_id

        json['text'] = self.text
        json['disable_link_preview'] = str(self.disable_link_preview).lower()
        
        if self.attachments:
            
            for att in self.attachments:

                if isinstance(att, InputMedia):
                    input_media = await self.__process_input_media(att)
                    json['attachments'].append(
                        input_media.model_dump()
                    ) 
                else:
                    json['attachments'].append(att.model_dump()) 
        
        if not self.link is None: json['link'] = self.link.model_dump()
        if not self.notify is None: json['notify'] = self.notify
        if not self.parse_mode is None: json['format'] = self.parse_mode.value

        response = None
        for attempt in range(5):
            response = await super().request(
                method=HTTPMethod.POST, 
                path=ApiPath.MESSAGES,
                model=SendedMessage,
                params=params,
                json=json
            )

            if isinstance(response, Error):
                if response.raw.get('code') == 'attachment.not.ready':
                    logger_bot.info(f'Ошибка при отправке загруженного медиа, попытка {attempt+1}, жду 2 секунды')
                    await asyncio.sleep(2)
                    continue
            
            return response
        return response