from typing import TYPE_CHECKING, List

from ..methods.types.added_members_chat import AddedMembersChat

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class AddMembersChat(BaseConnection):

    def __init__(
            self, 
            bot: 'Bot',
            chat_id: int,
            user_ids: List[int],

        ):
        self.bot = bot
        self.chat_id = chat_id
        self.user_ids = user_ids

    async def request(self) -> AddedMembersChat:
        json = {}

        json['user_ids'] = self.user_ids

        return await super().request(
            method=HTTPMethod.POST, 
            path=ApiPath.CHATS.value + '/' + str(self.chat_id) + ApiPath.MEMBERS,
            model=AddedMembersChat,
            params=self.bot.params,
            json=json
        )