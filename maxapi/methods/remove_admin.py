

from typing import TYPE_CHECKING

from .types.removed_admin import RemovedAdmin

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class RemoveAdmin(BaseConnection):

    def __init__(
            self, 
            bot: 'Bot',
            chat_id: int,
            user_id: int
        ):
        self.bot = bot
        self.chat_id = chat_id
        self.user_id = user_id

    async def request(self) -> RemovedAdmin:
        return await super().request(
            method=HTTPMethod.DELETE, 
            path=ApiPath.CHATS.value + '/' + str(self.chat_id) + \
                  ApiPath.MEMBERS + ApiPath.ADMINS + '/' + str(self.user_id),
            model=RemovedAdmin,
            params=self.bot.params,
        )