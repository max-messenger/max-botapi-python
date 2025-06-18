

from re import findall
from typing import TYPE_CHECKING, List

from .types.added_admin_chat import AddedListAdminChat

from ..types.users import ChatAdmin

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class AddAdminChat(BaseConnection):

    def __init__(
            self, 
            bot: 'Bot',
            chat_id: int,
            admins: List[ChatAdmin],
            marker: int = None
        ):
        self.bot = bot
        self.chat_id = chat_id
        self.admins = admins
        self.marker = marker

    async def request(self) -> AddedListAdminChat:
        json = {}

        json['admins'] = [admin.model_dump() for admin in self.admins]
        json['marker'] = self.marker

        return await super().request(
            method=HTTPMethod.POST, 
            path=ApiPath.CHATS.value + '/' + str(self.chat_id) + ApiPath.MEMBERS + ApiPath.ADMINS,
            model=AddedListAdminChat,
            params=self.bot.params,
            json=json
        )