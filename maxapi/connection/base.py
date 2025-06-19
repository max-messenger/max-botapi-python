import os
from typing import TYPE_CHECKING

import aiohttp
from pydantic import BaseModel

from ..types.errors import Error
from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath
from ..enums.upload_type import UploadType
from ..loggers import logger_bot, logger_connection

if TYPE_CHECKING:
    from ..bot import Bot


class BaseConnection:

    API_URL = 'https://botapi.max.ru'

    def __init__(self):
        self.bot: 'Bot' = None
        self.session: aiohttp.ClientSession = None

    async def request(
            self,
            method: HTTPMethod,
            path: ApiPath,
            model: BaseModel = None,
            is_return_raw: bool = False,
            **kwargs
        ):
        
        if not self.bot.session:
            self.bot.session = aiohttp.ClientSession(self.bot.API_URL)

        try:
            r = await self.bot.session.request(
                method=method.value, 
                url=path.value if isinstance(path, ApiPath) else path, 
                **kwargs
            )
        except aiohttp.ClientConnectorDNSError as e:
            return logger_connection.error(f'Ошибка при отправке запроса: {e}')

        if not r.ok:
            raw = await r.json()
            error = Error(code=r.status, raw=raw)
            logger_bot.error(error)
            return error
        
        raw = await r.json()

        if is_return_raw: return raw

        model = model(**raw)
        
        if hasattr(model, 'message'):
            attr = getattr(model, 'message')
            if hasattr(attr, 'bot'):
                attr.bot = self.bot
        
        if hasattr(model, 'bot'):
            model.bot = self.bot

        return model
    
    async def upload_file(
            self,
            url: str,
            path: str,
            type: UploadType
    ):
        with open(path, 'rb') as f:
            file_data = f.read()

        basename = os.path.basename(path)
        name, ext = os.path.splitext(basename)

        form = aiohttp.FormData()
        form.add_field(
            name='data',
            value=file_data,
            filename=basename,
            content_type=f"{type.value}/{ext.lstrip('.')}"
        )

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url=url, 
                data=form
            )

            return await response.text()