

from datetime import datetime
from typing import TYPE_CHECKING, List

from ..methods.types.getted_updates import process_update_request

from ..enums.update import UpdateType

from ..types.updates import Update

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

    async def request(self) -> Messages:
        params = self.bot.params.copy()

        params['limit'] = self.limit

        if self.bot.marker_updates:
            params['marker'] = self.bot.marker_updates

        event_json = await super().request(
            method=HTTPMethod.GET, 
            path=ApiPath.UPDATES,
            model=Messages,
            params=params,
            is_return_raw=True
        )

        return await process_update_request(
            event_json=event_json, 
            bot=self.bot
        )