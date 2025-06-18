import aiohttp
from pydantic import BaseModel

from ..types.errors import Error
from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath
from ..loggers import logger_bot


class BaseConnection:

    API_URL = 'https://botapi.max.ru'

    def __init__(self):
        self.bot = None
        self.session = None

    async def request(
            self,
            method: HTTPMethod,
            path: ApiPath,
            model: BaseModel,
            is_return_raw: bool = False,
            **kwargs
        ):
        
        if not self.bot.session:
            self.bot.session = aiohttp.ClientSession(self.bot.API_URL)

        r = await self.bot.session.request(
            method=method.value, 
            url=path.value if isinstance(path, ApiPath) else path, 
            **kwargs
        )

        if not r.ok:
            raw = await r.text()
            error = Error(code=r.status, text=raw)
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