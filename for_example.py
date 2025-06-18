from maxapi import F, Router
from maxapi.types import Command, MessageCreated

router = Router()


@router.message_created(Command('router'))
async def hello(obj: MessageCreated):
    file = __file__.split('\\')[-1]
    await obj.message.answer(f"Пишу тебе из роута {file}")