from typing import TYPE_CHECKING

from ..types.users import User

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class GetMe(BaseConnection):
    
    """
    Класс для получения информации о боте.

    Args:
        bot (Bot): Экземпляр бота для выполнения запроса.
    """
    
    def __init__(self, bot: 'Bot'):
        self.bot = bot

    async def request(self) -> User:
        
        """
        Выполняет GET-запрос для получения данных о боте.

        Returns:
            User: Объект пользователя с полной информацией.
        """
        
        return await super().request(
            method=HTTPMethod.GET, 
            path=ApiPath.ME,
            model=User,
            params=self.bot.params
        )