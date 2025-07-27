from typing import Any, Callable, Awaitable

class BaseMiddleware:
    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event_object: Any,
        data: dict[str, Any]
    ) -> Any:
        return await handler(event_object, data)