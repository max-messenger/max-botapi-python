

from typing import TYPE_CHECKING

from ..types.chats import Chats

from ..types.users import User

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class GetChats(BaseConnection):
    def __init__(
            self, 
            bot: 'Bot',
            count: int = 50,
            marker: int = None
        ):
        self.bot = bot
        self.count = count
        self.marker = marker

    async def request(self) -> Chats:
        params = self.bot.params.copy()

        params['count'] = self.count

        if self.marker: 
            params['marker'] = self.marker

        return await super().request(
            method=HTTPMethod.GET, 
            path=ApiPath.CHATS,
            model=Chats,
            params=params
        )