from typing import Any, Dict
from ..types.updates import UpdateUnion


class BaseMiddleware:
    def __init__(self):
        ...
    
    async def process_middleware(
            self, 
            result_data_kwargs: Dict[str, Any],
            event_object: UpdateUnion
        ):
        
        kwargs_temp = {'data': result_data_kwargs.copy()}
        
        for key in kwargs_temp.copy().keys():
            if not key in self.__call__.__annotations__.keys():
                del kwargs_temp[key]
        
        result: Dict[str, Any] = await self(event_object, **kwargs_temp)
        
        return result