from typing import TYPE_CHECKING

from .types.removed_admin import RemovedAdmin

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class RemoveAdmin(BaseConnection):
    
    """
    Класс для отмены прав администратора в чате.

    Args:
        bot (Bot): Экземпляр бота для выполнения запроса.
        chat_id (int): Идентификатор чата.
        user_id (int): Идентификатор пользователя.

    Attributes:
        bot (Bot): Экземпляр бота.
        chat_id (int): Идентификатор чата.
        user_id (int): Идентификатор пользователя.
    """

    def __init__(
            self, 
            bot: 'Bot',
            chat_id: int,
            user_id: int
        ):
        self.bot = bot
        self.chat_id = chat_id
        self.user_id = user_id

    async def request(self) -> RemovedAdmin:
        
        """
        Выполняет DELETE-запрос для отмены прав администратора в чате.

        Returns:
            RemovedAdmin: Объект с результатом отмены прав администратора.
        """
        
        return await super().request(
            method=HTTPMethod.DELETE, 
            path=ApiPath.CHATS + '/' + str(self.chat_id) + \
                  ApiPath.MEMBERS + ApiPath.ADMINS + '/' + str(self.user_id),
            model=RemovedAdmin,
            params=self.bot.params,
        )