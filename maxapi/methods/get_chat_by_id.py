from typing import TYPE_CHECKING

from ..types.chats import Chat

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class GetChatById(BaseConnection):

    def __init__(
            self, 
            bot: 'Bot',
            id: int
        ):
        self.bot = bot
        self.id = id

    async def request(self) -> Chat:
        return await super().request(
            method=HTTPMethod.GET, 
            path=ApiPath.CHATS.value + '/' + str(self.id),
            model=Chat,
            params=self.bot.params
        )