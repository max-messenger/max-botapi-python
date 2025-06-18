from typing import TYPE_CHECKING

from ..methods.types.deleted_bot_from_chat import DeletedBotFromChat
from ..methods.types.deleted_message import DeletedMessage

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath
from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class DeleteMeFromMessage(BaseConnection):
    def __init__(
            self,
            bot: 'Bot',
            chat_id: int,
        ):
            self.bot = bot
            self.chat_id = chat_id

    async def request(self) -> DeletedBotFromChat:
        return await super().request(
            method=HTTPMethod.DELETE, 
            path=ApiPath.CHATS + '/' + str(self.chat_id) + ApiPath.MEMBERS + ApiPath.ME,
            model=DeletedBotFromChat,
            params=self.bot.params,
        )