from typing import TYPE_CHECKING, Optional

from ..types.chats import Chats

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class GetChats(BaseConnection):
    
    """
    Класс для получения списка чатов через API.

    Args:
        bot (Bot): Экземпляр бота для выполнения запроса.
        count (int, optional): Максимальное количество чатов для получения. По умолчанию 50.
        marker (int, optional): Маркер для постраничной навигации. По умолчанию None.

    Attributes:
        bot (Bot): Экземпляр бота.
        count (int): Количество чатов для запроса.
        marker (int | None): Маркер для пагинации.
    """
    
    def __init__(
            self, 
            bot: 'Bot',
            count: int = 50,
            marker: Optional[int] = None
        ):
        self.bot = bot
        self.count = count
        self.marker = marker

    async def fetch(self) -> Chats:
        
        """
        Выполняет GET-запрос для получения списка чатов.

        Returns:
            Chats: Объект с данными по списку чатов.
        """
        
        if self.bot is None:
            raise RuntimeError('Bot не инициализирован')
        
        params = self.bot.params.copy()

        params['count'] = self.count

        if self.marker: 
            params['marker'] = self.marker

        return await super().request(
            method=HTTPMethod.GET, 
            path=ApiPath.CHATS,
            model=Chats,
            params=params
        )