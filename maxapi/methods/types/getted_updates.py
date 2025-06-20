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
            event_object.chat = await bot.get_chat_by_id(event_object.message.recipient.chat_id)
            event_object.from_user = event_object.callback.user
            
        case UpdateType.MESSAGE_CHAT_CREATED:
            event_object = MessageChatCreated(**event)
            event_object.chat = event_object.chat
            
        case UpdateType.MESSAGE_CREATED:
            event_object = MessageCreated(**event)
            event_object.chat = await bot.get_chat_by_id(event_object.message.recipient.chat_id)
            event_object.from_user = event_object.message.sender
            
        case UpdateType.MESSAGE_EDITED:
            event_object = MessageEdited(**event)
            event_object.chat = await bot.get_chat_by_id(event_object.message.recipient.chat_id)
            event_object.from_user = event_object.message.sender
            
        case UpdateType.MESSAGE_REMOVED:
            event_object = MessageRemoved(**event)
            event_object.chat = await bot.get_chat_by_id(event_object.chat_id)
            event_object.from_user = await bot.get_chat_member(
                chat_id=event_object.chat_id, 
                user_id=event_object.user_id
            )
            
        case UpdateType.USER_ADDED:
            event_object = UserAdded(**event)
            event_object.chat = await bot.get_chat_by_id(event_object.chat_id)
            event_object.from_user = event_object.user
            
        case UpdateType.USER_REMOVED:
            event_object = UserRemoved(**event)
            event_object.chat = await bot.get_chat_by_id(event_object.chat_id)
            event_object.from_user = await bot.get_chat_member(
                chat_id=event_object.chat_id, 
                user_id=event_object.admin_id
            ) if event_object.admin_id else None
            
    if event['update_type'] in (UpdateType.BOT_ADDED, 
                                UpdateType.BOT_REMOVED, 
                                UpdateType.BOT_STARTED, 
                                UpdateType.CHAT_TITLE_CHANGED):
        event_object.chat = await bot.get_chat_by_id(event_object.chat_id)
        event_object.from_user = event_object.user

    if hasattr(event_object, 'bot'):
        event_object.bot = bot
        
    if hasattr(event_object, 'message'):
        event_object.message.bot = bot
        
        for attachment in event_object.message.body.attachments:
            if hasattr(attachment, 'bot'):
                attachment.bot = bot
    
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