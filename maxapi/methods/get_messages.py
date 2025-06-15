

from typing import TYPE_CHECKING

from ..types.message import Messages
from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath
from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class GetMessages(BaseConnection):
    def __init__(self, bot: 'Bot', chat_id: int = None):
        self.bot = bot
        self.chat_id = chat_id

    async def request(self) -> Messages:
        params = self.bot.params.copy()

        if self.chat_id: params['chat_id'] = self.chat_id

        return await super().request(
            method=HTTPMethod.GET, 
            path=ApiPath.MESSAGES,
            model=Messages,
            params=params
        )