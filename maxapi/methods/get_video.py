from typing import List, TYPE_CHECKING

from ..types.attachments.video import Video

from .types.edited_message import EditedMessage
from ..types.message import NewMessageLink
from ..types.attachments.attachment import Attachment
from ..enums.parse_mode import ParseMode
from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath
from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class GetVideo(BaseConnection):
    def __init__(
            self,
            bot: 'Bot',
            video_token: str
        ):
            self.bot = bot
            self.video_token = video_token

    async def request(self) -> Video:

        return await super().request(
            method=HTTPMethod.GET, 
            path=ApiPath.VIDEOS.value + '/' + self.video_token,
            model=Video,
            params=self.bot.params,
        )