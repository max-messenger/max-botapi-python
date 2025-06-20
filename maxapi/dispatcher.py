from typing import Callable, List

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from uvicorn import Config, Server
from aiohttp import ClientConnectorError

from .filters.handler import Handler

from .context import MemoryContext
from .types.updates import UpdateUnion
from .types.errors import Error

from .methods.types.getted_updates import process_update_webhook, process_update_request

from .filters import filter_attrs

from .bot import Bot
from .enums.update import UpdateType
from .loggers import logger_dp


app = FastAPI()


class Dispatcher:
    
    """Основной класс для обработки событий бота.

    Обеспечивает работу с вебхуком и поллингом, управляет обработчиками событий.
    """
    
    def __init__(self):
        self.event_handlers: List[Handler] = []
        self.contexts: List[MemoryContext] = []
        self.bot = None
        self.on_started_func = None

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
        self.on_started = Event(update_type=UpdateType.ON_STARTED, router=self)
        
    async def check_me(self):
        
        """Проверяет и логирует информацию о боте."""
        
        me = await self.bot.get_me()
        logger_dp.info(f'Бот: @{me.username} id={me.user_id}')

    def include_routers(self, *routers: 'Router'):
        
        """Добавляет обработчики из роутеров.
        
        Args:
            *routers: Роутеры для включения
        """
        
        for router in routers:
            for event in router.event_handlers:
                self.event_handlers.append(event)

    def __get_memory_context(self, chat_id: int, user_id: int):
        
        """Возвращает или создает контекст для чата и пользователя.
        
        Args:
            chat_id: ID чата
            user_id: ID пользователя
            
        Returns:
            Существующий или новый контекст
        """

        for ctx in self.contexts:
            if ctx.chat_id == chat_id and ctx.user_id == user_id:
                return ctx
            
        new_ctx = MemoryContext(chat_id, user_id)
        self.contexts.append(new_ctx)
        return new_ctx

    async def handle(self, event_object: UpdateUnion):
        
        """Обрабатывает событие.
        
        Args:
            event_object: Объект события для обработки
        """
        
        is_handled = False

        for handler in self.event_handlers:

            if not handler.update_type == event_object.update_type:
                continue

            if handler.filters:
                if not filter_attrs(event_object, *handler.filters):
                    continue

            ids = event_object.get_ids()

            memory_context = self.__get_memory_context(*ids)
            
            if not handler.state == await memory_context.get_state() \
                and handler.state:
                continue
            
            func_args = handler.func_event.__annotations__.keys()

            kwargs = {'context': memory_context}

            for key in kwargs.copy().keys():
                if not key in func_args:
                    del kwargs[key]

            await handler.func_event(event_object, **kwargs)

            logger_dp.info(f'Обработано: {event_object.update_type} | chat_id: {ids[0]}, user_id: {ids[1]}')

            is_handled = True
            break

        if not is_handled:
            logger_dp.info(f'Проигнорировано: {event_object.update_type} | chat_id: {ids[0]}, user_id: {ids[1]}')

    async def start_polling(self, bot: Bot):
        
        """Запускает поллинг обновлений.
        
        Args:
            bot: Экземпляр бота
        """
        
        self.bot = bot
        await self.check_me()

        logger_dp.info(f'{len(self.event_handlers)} событий на обработку')

        if self.on_started_func:
            await self.on_started_func()

        while True:
            try:
                events = await self.bot.get_updates()

                if isinstance(events, Error):
                    logger_dp.info(f'Ошибка при получении обновлений: {events}')
                    continue

                self.bot.marker_updates = events.get('marker')

                processed_events = await process_update_request(
                    events=events,
                    bot=self.bot
                )
                
                for event in processed_events:
                    try:
                        await self.handle(event)
                    except Exception as e:
                        logger_dp.error(f"Ошибка при обработке события: {event.update_type}: {e}")
            except ClientConnectorError:
                logger_dp.error(f'Ошибка подключения: {e}')
            except Exception as e:
                logger_dp.error(f'Общая ошибка при обработке событий: {e}')

    async def handle_webhook(self, bot: Bot, host: str = '0.0.0.0', port: int = 8080):
        
        """Запускает вебхук сервер.
        
        Args:
            bot: Экземпляр бота
            host: Хост для сервера
            port: Порт для сервера
        """
        
        self.bot = bot
        await self.check_me()

        if self.on_started_func:
            await self.on_started_func()

        @app.post('/')
        async def _(request: Request):
            try:
                event_json = await request.json()

                event_object = await process_update_webhook(
                    event_json=event_json,
                    bot=self.bot
                )

                await self.handle(event_object)
                
                return JSONResponse(content={'ok': True}, status_code=200)
            except Exception as e:
                logger_dp.error(f"Ошибка при обработке события: {event_json['update_type']}: {e}")

        logger_dp.info(f'{len(self.event_handlers)} событий на обработку')
        config = Config(app=app, host=host, port=port, log_level="critical")
        server = Server(config)

        await server.serve()


class Router(Dispatcher):
    
    """Роутер для группировки обработчиков событий."""
    
    def __init__(self):
        super().__init__()


class Event:
    
    """Декоратор для регистрации обработчиков событий."""
    
    def __init__(self, update_type: UpdateType, router: Dispatcher | Router):
        self.update_type = update_type
        self.router = router

    def __call__(self, *args, **kwargs):
        def decorator(func_event: Callable):
            if self.update_type == UpdateType.ON_STARTED:
                self.router.on_started_func = func_event
            else:
                self.router.event_handlers.append(
                    Handler(
                        func_event=func_event, 
                        update_type=self.update_type,
                        *args, **kwargs
                    )
                )
            return func_event
            
        return decorator