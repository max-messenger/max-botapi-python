

from re import findall
from typing import TYPE_CHECKING

from ..methods.types.getted_list_admin_chat import GettedListAdminChat

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class GetListAdminChat(BaseConnection):

    def __init__(
            self, 
            bot: 'Bot',
            chat_id: int
        ):
        self.bot = bot
        self.chat_id = chat_id

    async def request(self) -> GettedListAdminChat:
        return await super().request(
            method=HTTPMethod.GET, 
            path=ApiPath.CHATS.value + '/' + str(self.chat_id) + ApiPath.MEMBERS + ApiPath.ADMINS,
            model=GettedListAdminChat,
            params=self.bot.params
        )