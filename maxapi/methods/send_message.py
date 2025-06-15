

from typing import List, TYPE_CHECKING

from ..enums.parse_mode import ParseMode

from ..types.message import NewMessageLink

from ..types.attachments.attachment import Attachment

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath
from .types.sended_message import SendedMessage
from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class SendMessage(BaseConnection):
    def __init__(
            self,
            bot: 'Bot',
            chat_id: int = None, 
            user_id: int = None, 
            disable_link_preview: bool = False,
            text: str = None,
            attachments: List[Attachment] = None,
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

    async def request(self) -> 'SendedMessage':
        params = self.bot.params.copy()

        json = {}

        if self.chat_id: params['chat_id'] = self.chat_id
        elif self.user_id: params['user_id'] = self.user_id

        json['text'] = self.text
        json['disable_link_preview'] = str(self.disable_link_preview).lower()
        
        if self.attachments: json['attachments'] = \
          [att.model_dump() for att in self.attachments]
        
        if not self.link is None: json['link'] = self.link.model_dump()
        if not self.notify is None: json['notify'] = self.notify
        if not self.parse_mode is None: json['format'] = self.parse_mode.value

        return await super().request(
            method=HTTPMethod.POST, 
            path=ApiPath.MESSAGES,
            model=SendedMessage,
            params=params,
            json=json
        )