from typing import TYPE_CHECKING

from ..methods.types.deleted_message import DeletedMessage

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath
from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class DeleteMessage(BaseConnection):
    
    """
    Класс для удаления сообщения через API.

    Args:
        bot (Bot): Экземпляр бота для выполнения запроса.
        message_id (str): Идентификатор сообщения, которое нужно удалить.
    """
    
    def __init__(
            self,
            bot: 'Bot',
            message_id: str,
        ):
            self.bot = bot
            self.message_id = message_id

    async def request(self) -> DeletedMessage:
        
        """
        Выполняет DELETE-запрос для удаления сообщения.

        Использует параметр message_id для идентификации сообщения.

        Returns:
            DeletedMessage: Результат операции удаления сообщения.
        """
        
        params = self.bot.params.copy()

        params['message_id'] = self.message_id

        return await super().request(
            method=HTTPMethod.DELETE, 
            path=ApiPath.MESSAGES,
            model=DeletedMessage,
            params=params,
        )