from __future__ import annotations

import os
import mimetypes

from typing import TYPE_CHECKING, Any, Optional
from uuid import uuid4

import aiofiles
import puremagic

from pydantic import BaseModel
from aiohttp import ClientSession, ClientConnectionError, FormData

from ..exceptions.invalid_token import InvalidToken
from ..exceptions.max import MaxConnection

from ..types.errors import Error
from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath
from ..enums.upload_type import UploadType

from ..loggers import logger_bot

if TYPE_CHECKING:
    from ..bot import Bot


class BaseConnection:
    
    """
    Базовый класс для всех методов API.

    Содержит общую логику выполнения запроса (например, сериализацию, отправку HTTP-запроса, обработку ответа).

    Метод request() может быть переопределён в потомках при необходимости.
    """

    API_URL = 'https://botapi.max.ru'
    RETRY_DELAY = 2
    ATTEMPTS_COUNT = 5
    AFTER_MEDIA_INPUT_DELAY = 2.0

    def __init__(self) -> None:
        self.bot: Optional[Bot] = None
        self.session: Optional[ClientSession] = None
        self.after_input_media_delay: float = self.AFTER_MEDIA_INPUT_DELAY

    async def request(
            self,
            method: HTTPMethod,
            path: ApiPath | str,
            model: BaseModel | Any = None,
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
        
        if self.bot is None:
            raise RuntimeError('Bot не инициализирован')
        
        if not self.bot.session:
            self.bot.session = ClientSession(
                base_url=self.bot.API_URL, 
                timeout=self.bot.default_connection.timeout, 
                **self.bot.default_connection.kwargs
            )

        try:
            r = await self.bot.session.request(
                method=method.value, 
                url=path.value if isinstance(path, ApiPath) else path, 
                **kwargs
            )
        except ClientConnectionError as e:
            raise MaxConnection(f'Ошибка при отправке запроса: {e}')
        
        if r.status == 401:
            await self.bot.session.close()
            raise InvalidToken('Неверный токен!')

        if not r.ok:
            raw = await r.json()
            error = Error(code=r.status, raw=raw)
            logger_bot.error(error)
            return error
        
        raw = await r.json()

        if is_return_raw: 
            return raw

        model = model(**raw) # type: ignore
        
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
        
        async with aiofiles.open(path, 'rb') as f:
            file_data = await f.read()

        basename = os.path.basename(path)
        _, ext = os.path.splitext(basename)

        form = FormData()
        form.add_field(
            name='data',
            value=file_data,
            filename=basename,
            content_type=f"{type.value}/{ext.lstrip('.')}"
        )

        async with ClientSession() as session:
            response = await session.post(
                url=url, 
                data=form
            )

            return await response.text()
        
    async def upload_file_buffer(
        self,
        url: str,
        buffer: bytes,
        type: UploadType
    ):
        """
        Загружает файл из буфера.

        :param url: Конечная точка загрузки файла
        :param buffer: Буфер (bytes)
        :param type: Тип файла (video, image, audio, file)

        :return: Сырой .text() ответ от сервера после загрузки файла
        """

        try:
            matches = puremagic.magic_string(buffer[:4096])
            if matches:
                mime_type = matches[0][1]
                ext = mimetypes.guess_extension(mime_type) or ''
            else:
                mime_type = f"{type.value}/*"
                ext = ''
        except Exception:
            mime_type = f"{type.value}/*"
            ext = ''

        basename = f'{uuid4()}{ext}'

        form = FormData()
        form.add_field(
            name='data',
            value=buffer,
            filename=basename,
            content_type=mime_type
        )

        async with ClientSession() as session:
            response = await session.post(
                url=url, 
                data=form
            )
            return await response.text()
        
    async def download_file(
            self,
            path: str,
            url: str,
            token: str,
    ):
        """
        Скачивает медиа с указанной ссылки по токену, сохраняя по определенному пути

        :param path: Путь сохранения медиа
        :param url: Ссылка на медиа
        :param token: Токен медиа

        :return: Числовой статус
        """
        
        headers = {
            'Authorization': f'Bearer {token}'
        }

        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                
                if response.status == 200:
                    async with aiofiles.open(path, 'wb') as f:
                        await f.write(await response.read())
                        
                return response.status