from typing import TYPE_CHECKING

from ..methods.types.deleted_message import DeletedMessage

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath
from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class DeleteMessage(BaseConnection):
    def __init__(
            self,
            bot: 'Bot',
            message_id: str,
        ):
            self.bot = bot
            self.message_id = message_id

    async def request(self) -> DeletedMessage:
        params = self.bot.params.copy()

        params['message_id'] = self.message_id

        return await super().request(
            method=HTTPMethod.DELETE, 
            path=ApiPath.MESSAGES,
            model=DeletedMessage,
            params=params,
        )