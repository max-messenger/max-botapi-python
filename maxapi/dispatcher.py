from __future__ import annotations

import asyncio

from typing import Any, Callable, Dict, List, TYPE_CHECKING

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from uvicorn import Config, Server
from aiohttp import ClientConnectorError

from .exceptions.invalid_token import InvalidToken

from .filters.middleware import BaseMiddleware
from .filters.handler import Handler

from .context import MemoryContext
from .types.updates import UpdateUnion
from .types.errors import Error

from .methods.types.getted_updates import process_update_webhook, process_update_request

from .filters import filter_attrs

from .bot import Bot
from .enums.update import UpdateType
from .loggers import logger_dp

if TYPE_CHECKING:
    from magic_filter import MagicFilter


webhook_app = FastAPI()

CONNECTION_RETRY_DELAY = 30
GET_UPDATES_RETRY_DELAY = 5


class Dispatcher:
    
    """
    Основной класс для обработки событий бота.

    Обеспечивает запуск поллинга и вебхука, маршрутизацию событий,
    применение middleware, фильтров и вызов соответствующих обработчиков.
    """
    
    def __init__(self):
        
        """
        Инициализация диспетчера.
        """
        
        self.event_handlers: List[Handler] = []
        self.contexts: List[MemoryContext] = []
        self.routers: List[Router] = []
        self.filters: List[MagicFilter] = []
        self.middlewares: List[BaseMiddleware] = []
        
        self.bot: Bot = None
        self.on_started_func: Callable = None

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
        
        """
        Проверяет и логирует информацию о боте.
        """
        
        me = await self.bot.get_me()
        
        self.bot._me = me
        
        logger_dp.info(f'Бот: @{me.username} first_name={me.first_name} id={me.user_id}')

    def include_routers(self, *routers: 'Router'):
        
        """
        Добавляет указанные роутеры в диспетчер.

        :param routers: Роутеры для добавления.
        """
        
        self.routers += [r for r in routers]
            
    async def __ready(self, bot: Bot):
        
        """
        Подготавливает диспетчер: сохраняет бота, регистрирует обработчики, вызывает on_started.

        :param bot: Экземпляр бота.
        """
        
        self.bot = bot
        
        await self.check_me()
        
        self.routers += [self]
        
        handlers_count = sum(len(router.event_handlers) for router in self.routers)

        logger_dp.info(f'{handlers_count} событий на обработку')

        if self.on_started_func:
            await self.on_started_func()
            
    def __get_memory_context(self, chat_id: int, user_id: int):
        
        """
        Возвращает существующий или создает новый контекст по chat_id и user_id.

        :param chat_id: Идентификатор чата.
        :param user_id: Идентификатор пользователя.
        :return: Объект MemoryContext.
        """

        for ctx in self.contexts:
            if ctx.chat_id == chat_id and ctx.user_id == user_id:
                return ctx
            
        new_ctx = MemoryContext(chat_id, user_id)
        self.contexts.append(new_ctx)
        return new_ctx
        
    async def process_middlewares(
            self,
            middlewares: List[BaseMiddleware],
            event_object: UpdateUnion,
            result_data_kwargs: Dict[str, Any]
        ):
        
        """
        Последовательно обрабатывает middleware цепочку.

        :param middlewares: Список middleware.
        :param event_object: Объект события.
        :param result_data_kwargs: Аргументы, передаваемые обработчику.
        :return: Изменённые аргументы или None.
        """
        
        for middleware in middlewares:
            result = await middleware.process_middleware(
                event_object=event_object,
                result_data_kwargs=result_data_kwargs
            )
            
            if result is None or result is False:
                return
            
            elif result is True:
                continue
            
            result_data_kwargs.update(result)
        
        return result_data_kwargs

    async def handle(self, event_object: UpdateUnion):
        
        """
        Основной обработчик события. Применяет фильтры, middleware и вызывает подходящий handler.

        :param event_object: Событие, пришедшее в бот.
        """
        
        try:
            ids = event_object.get_ids()
            memory_context = self.__get_memory_context(*ids)
            current_state = await memory_context.get_state()
            kwargs = {'context': memory_context}
            
            is_handled = False
            
            for router in self.routers:
                
                if is_handled:
                    break
                
                if router.filters:
                    if not filter_attrs(event_object, *router.filters):
                        continue
                    
                kwargs = await self.process_middlewares(
                    middlewares=router.middlewares,
                    event_object=event_object,
                    result_data_kwargs=kwargs
                )
                
                for handler in router.event_handlers:

                    if not handler.update_type == event_object.update_type:
                        continue

                    if handler.filters:
                        if not filter_attrs(event_object, *handler.filters):
                            continue

                    if not handler.state == current_state and handler.state:
                        continue
                    
                    func_args = handler.func_event.__annotations__.keys()
                    
                    kwargs = await self.process_middlewares(
                        middlewares=handler.middlewares,
                        event_object=event_object,
                        result_data_kwargs=kwargs
                    )
                    
                    if not kwargs:
                        continue
                        
                    for key in kwargs.copy().keys():
                        if not key in func_args:
                            del kwargs[key]
                        
                    await handler.func_event(event_object, **kwargs)

                    logger_dp.info(f'Обработано: {event_object.update_type} | chat_id: {ids[0]}, user_id: {ids[1]}')

                    is_handled = True
                    break

            if not is_handled:
                logger_dp.info(f'Проигнорировано: {event_object.update_type} | chat_id: {ids[0]}, user_id: {ids[1]}')
            
        except Exception as e:
            logger_dp.error(f"Ошибка при обработке события: {event_object.update_type} | chat_id: {ids[0]}, user_id: {ids[1]} | {e} ")

    async def start_polling(self, bot: Bot):
        
        """
        Запускает цикл получения обновлений с сервера (long polling).

        :param bot: Экземпляр бота.
        """
        
        await self.__ready(bot)

        while True:
            try:
                events = await self.bot.get_updates()

                if isinstance(events, Error):
                    logger_dp.info(f'Ошибка при получении обновлений: {events}, жду {GET_UPDATES_RETRY_DELAY} секунд')
                    await asyncio.sleep(GET_UPDATES_RETRY_DELAY)
                    continue

                self.bot.marker_updates = events.get('marker')

                processed_events = await process_update_request(
                    events=events,
                    bot=self.bot
                )
                
                for event in processed_events:
                    await self.handle(event)
                    
            except ClientConnectorError:
                logger_dp.error(f'Ошибка подключения, жду {CONNECTION_RETRY_DELAY} секунд')
                await asyncio.sleep(CONNECTION_RETRY_DELAY)
            except Exception as e:
                logger_dp.error(f'Общая ошибка при обработке событий: {e}')

    async def handle_webhook(self, bot: Bot, host: str = '0.0.0.0', port: int = 8080):
        
        """
        Запускает FastAPI-приложение для приёма обновлений через вебхук.

        :param bot: Экземпляр бота.
        :param host: Хост, на котором запускается сервер.
        :param port: Порт сервера.
        """

        @webhook_app.post('/')
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

        await self.init_serve(
            bot=bot,
            host=host,
            port=port
        )
        
    async def init_serve(self, bot: Bot, host: str = '0.0.0.0', port: int = 8080, **kwargs):
    
        """
        Запускает сервер для обработки входящих вебхуков.

        :param bot: Экземпляр бота.
        :param host: Хост, на котором запускается сервер.
        :param port: Порт сервера.
        """
        
        config = Config(app=webhook_app, host=host, port=port, **kwargs)
        server = Server(config)
        
        await self.__ready(bot)

        await server.serve()


class Router(Dispatcher):
    
    """
    Роутер для группировки обработчиков событий.
    """
    
    def __init__(self):
        super().__init__()


class Event:
    
    """
    Декоратор для регистрации обработчиков событий.
    """
    
    def __init__(self, update_type: UpdateType, router: Dispatcher | Router):
        
        """
        Инициализирует событие-декоратор.

        :param update_type: Тип события (UpdateType).
        :param router: Роутер или диспетчер, в который регистрируется обработчик.
        """
        
        self.update_type = update_type
        self.router = router

    def __call__(self, *args, **kwargs):
        
        """
        Регистрирует функцию как обработчик события.

        :return: Исходная функция.
        """
        
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