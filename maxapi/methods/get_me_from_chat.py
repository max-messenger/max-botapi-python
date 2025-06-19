

from typing import TYPE_CHECKING

from ..types.chats import ChatMember

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class GetMeFromChat(BaseConnection):
    def __init__(
            self, 
            bot: 'Bot',
            chat_id: int
        ):
        self.bot = bot
        self.chat_id = chat_id

    async def request(self) -> ChatMember:
        return await super().request(
            method=HTTPMethod.GET, 
            path=ApiPath.CHATS + '/' + str(self.chat_id) + ApiPath.MEMBERS + ApiPath.ME,
            model=ChatMember,
            params=self.bot.params
        )