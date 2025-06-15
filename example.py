from maxapi.bot import Bot
from maxapi.dispatcher import Dispatcher
from maxapi.types.updates.message_created import MessageCreated
from maxapi.types.updates.message_callback import MessageCallback
from maxapi.types.attachments.attachment import ButtonsPayload
from maxapi.types.attachments.buttons.callback_button import CallbackButton
from maxapi.types.attachments.attachment import Attachment
from maxapi.enums.attachment import AttachmentType
from maxapi.enums.button_type import ButtonType
from maxapi.enums.intent import Intent
from maxapi.filters import F


bot = Bot('токен')
dp = Dispatcher()

# Отвечает только на текст "Привет"
@dp.message_created(F.message.body.text == 'Привет')
async def hello(obj: MessageCreated):
    await obj.message.answer('Привет 👋')

# Отвечает только на текст "Клавиатура"
@dp.message_created(F.message.body.text == 'Клавиатура')
async def hello(obj: MessageCreated):
    button_1 = CallbackButton(type=ButtonType.CALLBACK, text='Кнопка 1', payload='1', intent=Intent.DEFAULT)
    button_2 = CallbackButton(type=ButtonType.CALLBACK, text='Кнопка 2', payload='2', intent=Intent.DEFAULT)

    keyboard = ButtonsPayload(buttons=[[button_1], [button_2]])

    attachments = [Attachment(type=AttachmentType.INLINE_KEYBOARD, payload=keyboard)]

    await obj.message.answer('Привет 👋', attachments=attachments)

# Ответчает на коллбек с начинкой "1"
@dp.message_callback(F.callback.payload == '1')
async def _(obj: MessageCallback):
    await obj.message.answer('Вы нажали на кнопку 1 🤩')

# Ответчает на коллбек с начинкой "2"
@dp.message_callback(F.callback.payload == '2')
async def _(obj: MessageCallback):
    await obj.message.answer('Вы нажали на кнопку 2 🥳')

# Отвечает на любое текстовое сообщение
@dp.message_created(F.message.body.text)
async def hello(obj: MessageCreated):
    await obj.message.answer(f'Повторяю за вами: {obj.message.body.text}')


dp.handle_webhook(bot)