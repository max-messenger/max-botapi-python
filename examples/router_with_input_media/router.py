from maxapi import F, Router
from maxapi.types import Command, MessageCreated
from maxapi.types import InputMedia

router = Router()
file = __file__.split('\\')[-1]


@router.message_created(Command('router'))
async def hello(obj: MessageCreated):
    await obj.message.answer(f"Пишу тебе из роута {file}")
    

# новая команда для примера, /media,
# пример использования: /media image.png (медиафайл берется указанному пути)
@router.message_created(Command('media'))
async def hello(event: MessageCreated):
    await event.message.answer(
        attachments=[
            InputMedia(
                path=event.message.body.text.replace('/media ', '')
            )
        ]
    )