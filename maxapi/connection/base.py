import os
from typing import TYPE_CHECKING

import aiohttp
from pydantic import BaseModel

from ..types.errors import Error
from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath
from ..enums.upload_type import UploadType
from ..loggers import logger_bot, logger_connection

if TYPE_CHECKING:
    from ..bot import Bot


class BaseConnection:
    
    """
    Базовый класс для всех методов API.

    Содержит общую логику выполнения запроса (например, сериализацию, отправку HTTP-запроса, обработку ответа).

    Метод request() может быть переопределён в потомках при необходимости.
    """

    API_URL = 'https://botapi.max.ru'

    def __init__(self):
        self.bot: 'Bot' = None
        self.session: aiohttp.ClientSession = None

    async def request(
            self,
            method: HTTPMethod,
            path: ApiPath,
            model: BaseModel = None,
            is_return_raw: bool = False,
            **kwargs
        ):
        
        """
        Выполняет HTTP-запрос к API, используя указанные параметры.

        :param method: HTTP-метод запроса (GET, POST и т.д.)
        :param path: Путь к конечной точке API
        :param model: Pydantic-модель, в которую будет десериализован ответ (если is_return_raw=False)
        :param is_return_raw: Если True — вернуть "сырое" тело ответа, иначе — результат десериализации в model
        :param kwargs: Дополнительные параметры (например, query, headers, json)

        :return:
            - Объект model (если is_return_raw=False и model задан)
            
            - dict (если is_return_raw=True)
        """
        
        if not self.bot.session:
            self.bot.session = aiohttp.ClientSession(self.bot.API_URL)

        try:
            r = await self.bot.session.request(
                method=method.value, 
                url=path.value if isinstance(path, ApiPath) else path, 
                **kwargs
            )
        except aiohttp.ClientConnectorDNSError as e:
            return logger_connection.error(f'Ошибка при отправке запроса: {e}')

        if not r.ok:
            raw = await r.json()
            error = Error(code=r.status, raw=raw)
            logger_bot.error(error)
            return error
        
        raw = await r.json()

        if is_return_raw: return raw

        model = model(**raw)
        
        if hasattr(model, 'message'):
            attr = getattr(model, 'message')
            if hasattr(attr, 'bot'):
                attr.bot = self.bot
        
        if hasattr(model, 'bot'):
            model.bot = self.bot

        return model
    
    async def upload_file(
            self,
            url: str,
            path: str,
            type: UploadType
    ):
        """
        Загружает файл на указанный URL.

        :param url: Конечная точка загрузки файла
        :param path: Путь к локальному файлу
        :param type: Тип файла (video, image, audio, file)

        :return: Сырой .text() ответ от сервера после загрузки файла
        """
        
        with open(path, 'rb') as f:
            file_data = f.read()

        basename = os.path.basename(path)
        _, ext = os.path.splitext(basename)

        form = aiohttp.FormData()
        form.add_field(
            name='data',
            value=file_data,
            filename=basename,
            content_type=f"{type.value}/{ext.lstrip('.')}"
        )

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url=url, 
                data=form
            )

            return await response.text()