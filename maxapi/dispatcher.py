from typing import Callable, List

import aiohttp
from fastapi.responses import JSONResponse
import uvicorn

from fastapi import FastAPI, Request
from magic_filter import MagicFilter

from .methods.types.getted_updates import process_update_webhook, process_update_request

from .filters import filter_m
from .types.updates import Update

from .bot import Bot
from .enums.update import UpdateType
from .types.updates.bot_added import BotAdded
from .types.updates.bot_removed import BotRemoved
from .types.updates.bot_started import BotStarted
from .types.updates.chat_title_changed import ChatTitleChanged
from .types.updates.message_callback import MessageCallback
from .types.updates.message_chat_created import MessageChatCreated
from .types.updates.message_created import MessageCreated
from .types.updates.message_edited import MessageEdited
from .types.updates.message_removed import MessageRemoved
from .types.updates.user_added import UserAdded
from .types.updates.user_removed import UserRemoved
from .loggers import logger


app = FastAPI()


class Handler:

    def __init__(
            self,
            *args,
            func_event: Callable,
            update_type: UpdateType,
            **kwargs
        ):
        
        self.func_event = func_event
        self.update_type = update_type
        self.filters = []

        for arg in args:
            if isinstance(arg, MagicFilter):
                arg: MagicFilter = arg

                self.filters.append(arg)


class Dispatcher:
    def __init__(self):
        self.event_handlers = []
        self.bot = None

        self.message_created = Event(update_type=UpdateType.MESSAGE_CREATED, router=self)
        self.bot_added = Event(update_type=UpdateType.BOT_ADDED, router=self)
        self.bot_removed = Event(update_type=UpdateType.BOT_REMOVED, router=self)
        self.bot_started = Event(update_type=UpdateType.BOT_STARTED, router=self)
        self.chat_title_changed = Event(update_type=UpdateType.CHAT_TITLE_CHANGED, router=self)
        self.message_callback = Event(update_type=UpdateType.MESSAGE_CALLBACK, router=self)
        self.message_chat_created = Event(update_type=UpdateType.MESSAGE_CHAT_CREATED, router=self)
        self.message_edited = Event(update_type=UpdateType.MESSAGE_EDITED, router=self)
        self.message_removed = Event(update_type=UpdateType.MESSAGE_REMOVED, router=self)
        self.user_added = Event(update_type=UpdateType.USER_ADDED, router=self)
        self.user_removed = Event(update_type=UpdateType.USER_REMOVED, router=self)

    def include_routers(self, *routers: 'Router'):
        for router in routers:
            for event in router.event_handlers:
                self.event_handlers.append(event)

    async def start_polling(self, bot: Bot):
        self.bot = bot
        self.bot.session = aiohttp.ClientSession(self.bot.API_URL)

        while True:
            try:
                events = await self.bot.get_updates()
                
                for event in events:
                    handlers: List[Handler] = self.event_handlers
                    for handler in handlers:

                        if not handler.update_type == event.update_type:
                            continue

                        if handler.filters:
                            if not filter_m(event, *handler.filters):
                                continue

                        await handler.func_event(event)
                        break
            except Exception as e:
                print(e)
                ...

        logger.info(f'{len(self.event_handlers)} event handlers started')

    def handle_webhook(self, bot: Bot, host: str = 'localhost', port: int = 8080):
        self.bot = bot
        self.bot.session = aiohttp.ClientSession(self.bot.API_URL)

        @app.post("/")
        async def _(request: Request):
            try:
                event_json = await request.json()

                event_object = await process_update_webhook(
                    event_json=event_json,
                    bot=self.bot
                )

                handlers: List[Handler] = self.event_handlers
                for handler in handlers:

                    if not handler.update_type == event_object.update_type:
                        continue

                    if handler.filters:
                        if not filter_m(event_object, *handler.filters):
                            continue

                    await handler.func_event(event_object)
                    break
                
                return JSONResponse(content={'ok': True}, status_code=200)
            except Exception as e:
                print(e)
                ...

        logger.info(f'{len(self.event_handlers)} event handlers started')
        uvicorn.run(app, host=host, port=port, log_level='critical')


class Router(Dispatcher):
    def __init__(self):
        super().__init__()


class Event:
    def __init__(self, update_type: UpdateType, router: Dispatcher | Router):
        self.update_type = update_type
        self.router = router

    def __call__(self, *args, **kwargs):
        def decorator(func_event: Callable):
            self.router.event_handlers.append(
                Handler(
                    func_event=func_event, 
                    update_type=self.update_type,
                    *args, **kwargs
                )
            )
            return func_event
            
        return decorator