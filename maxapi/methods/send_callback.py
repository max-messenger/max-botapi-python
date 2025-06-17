

from typing import List, TYPE_CHECKING

from ..methods.types.sended_callback import SendedCallback

from .types.sended_message import SendedMessage
from ..types.attachments.attachment import Attachment
from ..enums.parse_mode import ParseMode
from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath
from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot
    from ..types.message import Message


class SendCallback(BaseConnection):
    def __init__(
            self,
            bot: 'Bot',
            callback_id: str,
            message: 'Message' = None,
            notification: str = None
        ):
            self.bot = bot
            self.callback_id = callback_id
            self.message = message
            self.notification = notification

    async def request(self) -> SendedCallback:
        try:
            params = self.bot.params.copy()

            params['callback_id'] = self.callback_id

            json = {}
            
            if self.message: json['message'] = self.message.model_dump()
            if self.notification: json['notification'] = self.notification

            return await super().request(
                method=HTTPMethod.POST, 
                path=ApiPath.ANSWERS,
                model=SendedCallback,
                params=params,
                json=json
            )
        except Exception as e:
            print(e)
            ...