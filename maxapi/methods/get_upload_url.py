

from typing import TYPE_CHECKING

from ..methods.types.getted_upload_url import GettedUploadUrl
from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath
from ..enums.upload_type import UploadType
from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class GetUploadURL(BaseConnection):
    def __init__(
            self,
            bot: 'Bot',
            type: UploadType
        ):
        self.bot = bot
        self.type = type

    async def request(self) -> GettedUploadUrl:
        params = self.bot.params.copy()

        params['type'] = self.type.value

        return await super().request(
            method=HTTPMethod.POST, 
            path=ApiPath.UPLOADS,
            model=GettedUploadUrl,
            params=params,
        )