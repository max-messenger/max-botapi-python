

from datetime import datetime
from typing import TYPE_CHECKING, List

from .types.getted_pineed_message import GettedPin

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath
from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class GetPinnedMessage(BaseConnection):
    def __init__(
            self,
            bot: 'Bot', 
            chat_id: int,
        ):
        self.bot = bot
        self.chat_id = chat_id

    async def request(self) -> GettedPin:
        return await super().request(
            method=HTTPMethod.GET, 
            path=ApiPath.CHATS + '/' + str(self.chat_id) + ApiPath.PIN,
            model=GettedPin,
            params=self.bot.params
        )