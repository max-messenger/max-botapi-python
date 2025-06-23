import asyncio
import logging

from typing import Any, Dict

from maxapi import Bot, Dispatcher
from maxapi.filters.middleware import BaseMiddleware
from maxapi.types import MessageCreated, Command, UpdateUnion
from maxapi.types.command import Command

logging.basicConfig(level=logging.INFO)

bot = Bot(token='тут_ваш_токен')
dp = Dispatcher()


class CheckChatTitleMiddleware(BaseMiddleware):
    async def __call__(
            self, 
            event: UpdateUnion,
        ):
        
        return event.chat.title == 'MAXApi'


@dp.message_created(Command('start'), CheckChatTitleMiddleware())
async def start(event: MessageCreated):
    await event.message.answer('Это сообщение было отправлено, так как ваш чат называется "MAXApi"!')
    
    
class CustomDataMiddleware(BaseMiddleware):
    async def __call__(
            self, 
            event: UpdateUnion,
            data: Dict[str, Any]
        ):
        
        data['custom_data'] = f'Это ID того кто вызвал команду: {event.from_user.user_id}'
        
        return data
    

@dp.message_created(Command('custom_data'), CustomDataMiddleware())
async def custom_data(event: MessageCreated, custom_data: str):
    await event.message.answer(custom_data)
    
    
@dp.message_created(Command('many_middlewares'), CheckChatTitleMiddleware(), CustomDataMiddleware())
async def many_middlewares(event: MessageCreated, custom_data: str):
    await event.message.answer('Это сообщение было отправлено, так как ваш чат называется "MAXApi"!')
    await event.message.answer(custom_data)
    

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())