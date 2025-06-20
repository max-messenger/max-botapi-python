

from typing import TYPE_CHECKING

from ..methods.types.sended_callback import SendedCallback

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot
    from ..types.message import Message


class SendCallback(BaseConnection):
    
    """
    Класс для отправки callback-ответа с опциональным сообщением и уведомлением.

    Args:
        bot (Bot): Экземпляр бота для выполнения запроса.
        callback_id (str): Идентификатор callback.
        message (Message, optional): Сообщение для отправки в ответе.
        notification (str, optional): Текст уведомления.

    Attributes:
        bot (Bot): Экземпляр бота.
        callback_id (str): Идентификатор callback.
        message (Message | None): Сообщение для отправки.
        notification (str | None): Текст уведомления.
    """
    
    def __init__(
            self,
            bot: 'Bot',
            callback_id: str,
            message: 'Message' = None,
            notification: str = None
        ):
            self.bot = bot
            self.callback_id = callback_id
            self.message = message
            self.notification = notification

    async def request(self) -> SendedCallback:
        
        """
        Выполняет POST-запрос для отправки callback-ответа.

        Возвращает результат отправки.

        Returns:
            SendedCallback: Объект с результатом отправки callback.
        """
        
        params = self.bot.params.copy()

        params['callback_id'] = self.callback_id

        json = {}
        
        if self.message: json['message'] = self.message.model_dump()
        if self.notification: json['notification'] = self.notification

        return await super().request(
            method=HTTPMethod.POST, 
            path=ApiPath.ANSWERS,
            model=SendedCallback,
            params=params,
            json=json
        )