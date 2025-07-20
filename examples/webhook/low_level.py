import asyncio
import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from maxapi import Bot, Dispatcher
from maxapi.methods.types.getted_updates import process_update_webhook
from maxapi.types import MessageCreated
from maxapi.dispatcher import webhook_app

logging.basicConfig(level=logging.INFO)

bot = Bot('тут_ваш_токен')
dp = Dispatcher()

 
@dp.message_created()
async def handle_message(event: MessageCreated):
    await event.message.answer('Бот работает через вебхук!')

# Регистрация обработчика
# для вебхука
@webhook_app.post('/')
async def _(request: Request):
    
    # Сериализация полученного запроса
    event_json = await request.json()
    
    # Десериализация полученного запроса
    # в pydantic
    event_object = await process_update_webhook(
        event_json=event_json,
        bot=bot
    )
    
    # ...свой код
    print(f'Информация из вебхука: {event_json}')
    # ...свой код

    # Окончательная обработка запроса
    await dp.handle(event_object)
    
    # Ответ вебхука
    return JSONResponse(content={'ok': True}, status_code=200)


async def main():
    
    # Запуск сервера
    await dp.init_serve(bot, log_level='critical')


if __name__ == '__main__':
    asyncio.run(main())
