import aiohttp
from pydantic import BaseModel

from ..types.errors import Error
from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath


class BaseConnection:

    API_URL = 'https://botapi.max.ru'

    async def request(
            self,
            method: HTTPMethod,
            path: ApiPath,
            model: BaseModel,
            is_return_raw: bool = False,
            **kwargs
        ):
        async with aiohttp.ClientSession(self.API_URL) as s:
            r = await s.request(
                method=method.value, 
                url=path.value, 
                **kwargs
            )

            if not r.ok:
                raw = await r.text()
                return Error(code=r.status, text=raw)
            
            raw = await r.json()

            if is_return_raw: return raw

            return model(**raw)