import asyncio
import logging
from maxapi.bot import Bot
from maxapi.dispatcher import Dispatcher
from maxapi.types.updates.message_created import MessageCreated
from maxapi.filters import F

logging.basicConfig(level=logging.INFO)
bot = Bot('токен')
dp = Dispatcher()


# Отвечает на лю
# любое текстовое сообщение
@dp.message_created(F.message.body.text)
async def hello(obj: MessageCreated):
    await obj.message.answer(f'Повторяю за вами: {obj.message.body.text}')


async def main():
    await dp.start_polling(bot)

asyncio.run(main())