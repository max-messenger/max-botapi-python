

from logging import getLogger
from typing import TYPE_CHECKING, Any, Dict, Optional
from collections import Counter

from ..exceptions.max import MaxIconParamsException

from ..types.attachments.image import PhotoAttachmentRequestPayload
from ..types.chats import Chat

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection

logger = getLogger(__name__)


if TYPE_CHECKING:
    from ..bot import Bot


class EditChat(BaseConnection):
    
    """
    Класс для редактирования информации о чате через API.

    Args:
        bot (Bot): Экземпляр бота для выполнения запроса.
        chat_id (int): Идентификатор чата для редактирования.
        icon (PhotoAttachmentRequestPayload, optional): Новый значок (иконка) чата.
        title (str, optional): Новое название чата.
        pin (str, optional): Идентификатор закреплённого сообщения.
        notify (bool, optional): Включение или отключение уведомлений (по умолчанию True).
    """
    
    def __init__(
            self,
            bot: 'Bot',
            chat_id: int,
            icon: Optional[PhotoAttachmentRequestPayload] = None,
            title: Optional[str] = None,
            pin: Optional[str] = None,
            notify: Optional[bool] = None,
        ):
            self.bot = bot
            self.chat_id = chat_id
            self.icon = icon
            self.title = title
            self.pin = pin
            self.notify = notify

    async def fetch(self) -> Chat:
        
        """
        Выполняет PATCH-запрос для обновления параметров чата.

        Валидация:
            - Проверяется, что в `icon` атрибуты модели взаимоисключающие (в модели должно быть ровно 2 поля с None).
            - Если условие не выполнено, логируется ошибка и запрос не отправляется.

        Returns:
            Chat: Обновлённый объект чата.
        """
        
        assert self.bot is not None
        json: Dict[str, Any] = {}

        if self.icon:
            dump = self.icon.model_dump()
            counter = Counter(dump.values())

            if not None in counter or \
                not counter[None] == 2:
                    
                raise MaxIconParamsException(
                    'Все атрибуты модели Icon являются взаимоисключающими | '
                    'https://dev.max.ru/docs-api/methods/PATCH/chats/-chatId-'
                )
            
            json['icon'] = dump

        if self.title: json['title'] = self.title
        if self.pin: json['pin'] = self.pin
        if self.notify: json['notify'] = self.notify

        return await super().request(
            method=HTTPMethod.PATCH, 
            path=ApiPath.CHATS.value + '/' + str(self.chat_id),
            model=Chat,
            params=self.bot.params,
            json=json
        )