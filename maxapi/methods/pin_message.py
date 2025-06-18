

from datetime import datetime
from typing import TYPE_CHECKING, List

from .types.pinned_message import PinnedMessage

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath
from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class PinMessage(BaseConnection):
    def __init__(
            self,
            bot: 'Bot', 
            chat_id: int,
            message_id: str,
            notify: bool = True
        ):
        self.bot = bot
        self.chat_id = chat_id
        self.message_id = message_id
        self.notify = notify

    async def request(self) -> PinnedMessage:
        json = {}

        json['message_id'] = self.message_id
        json['notify'] = self.notify

        return await super().request(
            method=HTTPMethod.PUT, 
            path=ApiPath.CHATS + '/' + str(self.chat_id) + ApiPath.PIN,
            model=PinnedMessage,
            params=self.bot.params,
            json=json
        )