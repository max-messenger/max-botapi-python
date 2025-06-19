import asyncio
import logging

from maxapi import Bot, Dispatcher, F
from maxapi.context import MemoryContext, State, StatesGroup
from maxapi.types import Command, MessageCreated, CallbackButton, MessageCallback
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

from example.for_example import router

logging.basicConfig(level=logging.INFO)

bot = Bot('токен')
dp = Dispatcher()
dp.include_routers(router)


start_text = '''Мои команды:

/clear очищает ваш контекст
/state или /context показывают ваше контекстное состояние
/data показывает вашу контекстную память
'''


class Form(StatesGroup):
    name = State()
    age = State()


@dp.on_started()
async def _():
    logging.info('Бот стартовал!')


@dp.message_created(Command('clear'))
async def hello(obj: MessageCreated, context: MemoryContext):
    await context.clear()
    await obj.message.answer(f"Ваш контекст был очищен!")


@dp.message_created(Command('data'))
async def hello(obj: MessageCreated, context: MemoryContext):
    data = await context.get_data()
    await obj.message.answer(f"Ваша контекстная память: {str(data)}")


@dp.message_created(Command('context'))
@dp.message_created(Command('state'))
async def hello(obj: MessageCreated, context: MemoryContext):
    data = await context.get_state()
    await obj.message.answer(f"Ваше контекстное состояние: {str(data)}")


@dp.message_created(Command('start'))
async def hello(obj: MessageCreated):
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(
            text='Ввести свое имя',
            payload='btn_1'
        ),
        CallbackButton(
            text='Ввести свой возраст',
            payload='btn_2'
        )
    )
    builder.row(
        CallbackButton(
            text='Не хочу',
            payload='btn_3'
        )
    )

    await obj.message.answer(
        text=start_text, 
        attachments=[builder.as_markup()] #  Для MAX клавиатура это вложение, 
    )                                    # поэтому она в списке вложений
    

@dp.message_callback(F.callback.payload == 'btn_1')
async def hello(obj: MessageCallback, context: MemoryContext):
    await context.set_state(Form.name)
    await obj.message.delete()
    await obj.message.answer(f'Отправьте свое имя:')


@dp.message_callback(F.callback.payload == 'btn_2')
async def hello(obj: MessageCallback, context: MemoryContext):
    await context.set_state(Form.age)
    await obj.message.delete()
    await obj.message.answer(f'Отправьте ваш возраст:')


@dp.message_callback(F.callback.payload == 'btn_3')
async def hello(obj: MessageCallback, context: MemoryContext):
    await obj.message.delete()
    await obj.message.answer(f'Ну ладно 🥲')


@dp.message_created(F.message.body.text, Form.name)
async def hello(obj: MessageCreated, context: MemoryContext):
    await context.update_data(name=obj.message.body.text)

    data = await context.get_data()

    await obj.message.answer(f"Приятно познакомиться, {data['name'].title()}!")
    

@dp.message_created(F.message.body.text, Form.age)
async def hello(obj: MessageCreated, context: MemoryContext):
    await context.update_data(age=obj.message.body.text)

    await obj.message.answer(f"Ого! А мне всего пару недель 😁")


async def main():
    await dp.start_polling(bot)
    # await dp.handle_webhook(
    #     bot=bot,
    #     host='localhost',
    #     port=8080
    # )


asyncio.run(main())