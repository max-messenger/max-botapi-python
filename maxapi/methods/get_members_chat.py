from typing import TYPE_CHECKING, List

from ..methods.types.getted_members_chat import GettedMembersChat

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class GetMembersChat(BaseConnection):
    
    """
    Класс для получения списка участников чата через API.

    Args:
        bot (Bot): Экземпляр бота для выполнения запроса.
        chat_id (int): Идентификатор чата.
        user_ids (List[str], optional): Список ID пользователей для фильтрации. По умолчанию None.
        marker (int, optional): Маркер для пагинации (начальная позиция). По умолчанию None.
        count (int, optional): Максимальное количество участников для получения. По умолчанию None.

    Attributes:
        bot (Bot): Экземпляр бота.
        chat_id (int): Идентификатор чата.
        user_ids (List[str] | None): Список ID пользователей для фильтра.
        marker (int | None): Позиция для пагинации.
        count (int | None): Максимальное количество участников.
    """

    def __init__(
            self, 
            bot: 'Bot',
            chat_id: int,
            user_ids: List[str] = None,
            marker: int = None,
            count: int = None,

        ):
        self.bot = bot
        self.chat_id = chat_id
        self.user_ids = user_ids
        self.marker = marker
        self.count = count

    async def request(self) -> GettedMembersChat:
        
        """
        Выполняет GET-запрос для получения участников чата с опциональной фильтрацией.

        Формирует параметры запроса с учётом фильтров и передаёт их базовому методу.

        Returns:
            GettedMembersChat: Объект с данными по участникам чата.
        """
        
        params = self.bot.params.copy()

        if self.user_ids: 
            self.user_ids = [str(user_id) for user_id in self.user_ids]
            params['user_ids'] = ','.join(self.user_ids)
        if self.marker: params['marker'] = self.marker
        if self.count: params['marker'] = self.count

        return await super().request(
            method=HTTPMethod.GET, 
            path=ApiPath.CHATS.value + '/' + str(self.chat_id) + ApiPath.MEMBERS,
            model=GettedMembersChat,
            params=params
        )