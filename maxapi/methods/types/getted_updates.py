from typing import TYPE_CHECKING

from ...enums.update import UpdateType
from ...types.updates.bot_added import BotAdded
from ...types.updates.bot_removed import BotRemoved
from ...types.updates.bot_started import BotStarted
from ...types.updates.chat_title_changed import ChatTitleChanged
from ...types.updates.message_callback import MessageCallback
from ...types.updates.message_chat_created import MessageChatCreated
from ...types.updates.message_created import MessageCreated
from ...types.updates.message_edited import MessageEdited
from ...types.updates.message_removed import MessageRemoved
from ...types.updates.user_added import UserAdded
from ...types.updates.user_removed import UserRemoved

if TYPE_CHECKING:
    from ...bot import Bot


async def get_update_model(event: dict, bot: 'Bot'):
    event_object = None
    match event['update_type']:
        case UpdateType.BOT_ADDED:
            event_object = BotAdded(**event)
        case UpdateType.BOT_REMOVED:
            event_object = BotRemoved(**event)
        case UpdateType.BOT_STARTED:
            event_object = BotStarted(**event)
        case UpdateType.CHAT_TITLE_CHANGED:
            event_object = ChatTitleChanged(**event)
        case UpdateType.MESSAGE_CALLBACK:
            event_object = MessageCallback(**event)
        case UpdateType.MESSAGE_CHAT_CREATED:
            event_object = MessageChatCreated(**event)
        case UpdateType.MESSAGE_CREATED:
            event_object = MessageCreated(**event)
        case UpdateType.MESSAGE_EDITED:
            event_object = MessageEdited(**event)
        case UpdateType.MESSAGE_REMOVED:
            event_object = MessageRemoved(**event)
        case UpdateType.USER_ADDED:
            event_object = UserAdded(**event)
        case UpdateType.USER_REMOVED:
            event_object = UserRemoved(**event)

    if hasattr(event_object, 'bot'):
        event_object.bot = bot
    if hasattr(event_object, 'message'):
        event_object.message.bot = bot
    
    return event_object


async def process_update_request(events: dict, bot: 'Bot'):
    events = [event for event in events['updates']]
    
    objects = []

    for event in events:
        
        objects.append(
            await get_update_model(
                bot=bot,
                event=event
            )
        )

    return objects


async def process_update_webhook(event_json: dict, bot: 'Bot'):
    return await get_update_model(
        bot=bot,
        event=event_json
    )