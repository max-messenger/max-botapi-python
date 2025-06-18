import aiohttp
from pydantic import BaseModel

from ..types.errors import Error
from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath


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
        s = self.bot.session
        r = await s.request(
            method=method.value, 
            url=path.value if isinstance(path, ApiPath) else path, 
            **kwargs
        )

        if not r.ok:
            raw = await r.text()
            return Error(code=r.status, text=raw)
        
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