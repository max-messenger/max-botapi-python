from typing import TYPE_CHECKING

from ..methods.types.deleted_pin_message import DeletedPinMessage

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class DeletePinMessage(BaseConnection):
    
    """
    Класс для удаления закреплённого сообщения в чате через API.

    Args:
        bot (Bot): Экземпляр бота для выполнения запроса.
        chat_id (str): Идентификатор чата, из которого нужно удалить закреплённое сообщение.
    """
    
    def __init__(
            self,
            bot: 'Bot',
            chat_id: str,
        ):
            self.bot = bot
            self.chat_id = chat_id

    async def request(self) -> DeletedPinMessage:
        
        """
        Выполняет DELETE-запрос для удаления закреплённого сообщения.

        Returns:
            DeletedPinMessage: Результат операции удаления закреплённого сообщения.
        """
        
        return await super().request(
            method=HTTPMethod.DELETE, 
            path=ApiPath.CHATS + '/' + str(self.chat_id) + ApiPath.PIN,
            model=DeletedPinMessage,
            params=self.bot.params,
        )