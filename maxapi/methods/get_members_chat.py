

from re import findall
from typing import TYPE_CHECKING, List

from ..methods.types.getted_members_chat import GettedMembersChat

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class GetMembersChat(BaseConnection):

    def __init__(
            self, 
            bot: 'Bot',
            chat_id: int,
            user_ids: List[str] = None,
            marker: int = None,
            count: int = None,

        ):
        self.bot = bot
        self.chat_id = chat_id
        self.user_ids = user_ids
        self.marker = marker
        self.count = count

    async def request(self) -> GettedMembersChat:
        params = self.bot.params.copy()

        if self.user_ids: params['user_ids'] = ','.join(self.user_ids)
        if self.marker: params['marker'] = self.marker
        if self.count: params['marker'] = self.count

        return await super().request(
            method=HTTPMethod.GET, 
            path=ApiPath.CHATS.value + '/' + str(self.chat_id) + ApiPath.MEMBERS,
            model=GettedMembersChat,
            params=params
        )