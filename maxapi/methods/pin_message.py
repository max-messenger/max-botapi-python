from typing import TYPE_CHECKING

from .types.pinned_message import PinnedMessage

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class PinMessage(BaseConnection):
    
    """
    Класс для закрепления сообщения в чате.

    Args:
        bot (Bot): Экземпляр бота для выполнения запроса.
        chat_id (int): Идентификатор чата, в котором закрепляется сообщение.
        message_id (str): Идентификатор сообщения для закрепления.
        notify (bool, optional): Отправлять ли уведомление о закреплении (по умолчанию True).

    Attributes:
        bot (Bot): Экземпляр бота.
        chat_id (int): Идентификатор чата.
        message_id (str): Идентификатор закрепляемого сообщения.
        notify (bool): Флаг отправки уведомления.
    """
    
    def __init__(
            self,
            bot: 'Bot', 
            chat_id: int,
            message_id: str,
            notify: bool = True
        ):
        self.bot = bot
        self.chat_id = chat_id
        self.message_id = message_id
        self.notify = notify

    async def request(self) -> PinnedMessage:
        
        """
        Выполняет PUT-запрос для закрепления сообщения в чате.

        Формирует тело запроса с ID сообщения и флагом уведомления.

        Returns:
            PinnedMessage: Объект с информацией о закреплённом сообщении.
        """
        
        json = {}

        json['message_id'] = self.message_id
        json['notify'] = self.notify

        return await super().request(
            method=HTTPMethod.PUT, 
            path=ApiPath.CHATS + '/' + str(self.chat_id) + ApiPath.PIN,
            model=PinnedMessage,
            params=self.bot.params,
            json=json
        )