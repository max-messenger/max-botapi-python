

from datetime import datetime
from typing import TYPE_CHECKING, List

from ..types.updates import UpdateUnion

from ..methods.types.getted_updates import process_update_request


from ..types.message import Messages
from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath
from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class GetUpdates(BaseConnection):
    def __init__(
            self,
            bot: 'Bot', 
            limit: int = 100,
        ):
        self.bot = bot
        self.limit = limit

    async def request(self) -> UpdateUnion:
        params = self.bot.params.copy()

        params['limit'] = self.limit

        event_json = await super().request(
            method=HTTPMethod.GET, 
            path=ApiPath.UPDATES,
            model=None,
            params=params,
            is_return_raw=True
        )

        return event_json