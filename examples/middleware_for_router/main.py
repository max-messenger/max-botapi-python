import asyncio
import logging

from typing import Any, Dict

from maxapi import Bot, Dispatcher
from maxapi.types import MessageCreated, Command, UpdateUnion
from maxapi.filters.middleware import BaseMiddleware

logging.basicConfig(level=logging.INFO)

bot = Bot(token='тут_ваш_токен')
dp = Dispatcher()


class CustomDataForRouterMiddleware(BaseMiddleware):
    async def __call__(
            self, 
            event: UpdateUnion,
            data: Dict[str, Any]
        ):
        
        data['custom_data'] = f'Это ID того кто вызвал команду: {event.from_user.user_id}'
        
        return data
    

@dp.message_created(Command('custom_data'))
async def custom_data(event: MessageCreated, custom_data: str):
    await event.message.answer(custom_data)
    
    
async def main():
    dp.middlewares = [
        CustomDataForRouterMiddleware()
    ]
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())