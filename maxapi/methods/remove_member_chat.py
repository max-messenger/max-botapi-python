from typing import TYPE_CHECKING, List

from .types.removed_member_chat import RemovedMemberChat

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class RemoveMemberChat(BaseConnection):

    def __init__(
            self, 
            bot: 'Bot',
            chat_id: int,
            user_id: int,
            block: bool = False,

        ):
        self.bot = bot
        self.chat_id = chat_id
        self.user_id = user_id
        self.block = block

    async def request(self) -> RemovedMemberChat:
        params = self.bot.params.copy()

        params['chat_id'] = self.chat_id
        params['user_id'] = self.user_id
        params['block'] = str(self.block).lower()

        return await super().request(
            method=HTTPMethod.DELETE, 
            path=ApiPath.CHATS.value + '/' + str(self.chat_id) + ApiPath.MEMBERS,
            model=RemovedMemberChat,
            params=params,
        )