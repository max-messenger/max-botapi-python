import asyncio

from typing import Any, Dict

from ..context.state_machine import State, StatesGroup


class MemoryContext:
    def __init__(self, chat_id: int, user_id: int):
        self.chat_id = chat_id
        self.user_id = user_id
        self._context: Dict[str, Any] = {}
        self._state: State | None = None
        self._lock = asyncio.Lock()

    async def get_data(self) -> dict[str, Any]:
        async with self._lock:
            return self._context

    async def set_data(self, data: dict[str, Any]):
        async with self._lock:
            self._context = data

    async def update_data(self, **kwargs):
        async with self._lock:
            self._context.update(kwargs)

    async def set_state(self, state: State | str = None):
        async with self._lock:
            self._state = state

    async def get_state(self):
        async with self._lock:
            return self._state

    async def clear(self):
        async with self._lock:
            self._state = None
            self._context = {}
