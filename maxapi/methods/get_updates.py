from typing import TYPE_CHECKING

from ..types.updates import UpdateUnion

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class GetUpdates(BaseConnection):
    
    """
    Класс для получения обновлений (updates) из API.

    Args:
        bot (Bot): Экземпляр бота для выполнения запроса.
        limit (int, optional): Максимальное количество обновлений для получения. По умолчанию 100.

    Attributes:
        bot (Bot): Экземпляр бота.
        limit (int): Лимит на количество обновлений.
    """
    
    def __init__(
            self,
            bot: 'Bot', 
            limit: int = 100,
        ):
        self.bot = bot
        self.limit = limit

    async def request(self) -> UpdateUnion:
        
        """
        Выполняет GET-запрос для получения обновлений с указанным лимитом.

        Возвращает необработанный JSON с обновлениями.

        Returns:
            UpdateUnion: Объединённый тип данных обновлений.
        """
        
        params = self.bot.params.copy()

        params['limit'] = self.limit

        event_json = await super().request(
            method=HTTPMethod.GET, 
            path=ApiPath.UPDATES,
            model=None,
            params=params,
            is_return_raw=True
        )

        return event_json