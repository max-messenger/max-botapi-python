from typing import TYPE_CHECKING

from ..methods.types.deleted_chat import DeletedChat

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath
from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class DeleteChat(BaseConnection):
    def __init__(
            self,
            bot: 'Bot',
            chat_id: int
        ):
            self.bot = bot
            self.chat_id = chat_id

    async def request(self) -> DeletedChat:
        return await super().request(
            method=HTTPMethod.DELETE, 
            path=ApiPath.CHATS.value + '/' + str(self.chat_id),
            model=DeletedChat,
            params=self.bot.params
        )