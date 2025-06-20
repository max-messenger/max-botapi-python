from re import findall
from typing import TYPE_CHECKING

from ..types.chats import Chat

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class GetChatByLink(BaseConnection):
    
    """
    Класс для получения информации о чате по ссылке.

    Args:
        bot (Bot): Экземпляр бота для выполнения запроса.
        link (str): Ссылка на чат (с содержанием @ или без).

    Attributes:
        link (list[str]): Список валидных частей ссылки.
        PATTERN_LINK (str): Регулярное выражение для парсинга ссылки.
    """

    PATTERN_LINK = r'@?[a-zA-Z]+[a-zA-Z0-9-_]*'

    def __init__(
            self, 
            bot: 'Bot',
            link: str
        ):
        self.bot = bot
        self.link = findall(self.PATTERN_LINK, link)

        if not self.link:
            return

    async def request(self) -> Chat:
        
        """
        Выполняет GET-запрос для получения данных чата по ссылке.

        Returns:
            Chat: Объект с информацией о чате.
        """
        
        return await super().request(
            method=HTTPMethod.GET, 
            path=ApiPath.CHATS.value + '/' + self.link[-1],
            model=Chat,
            params=self.bot.params
        )