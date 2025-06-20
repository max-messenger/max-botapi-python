from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field

from .update import Update

from ...types.users import User


if TYPE_CHECKING:
    from ...bot import Bot


class UserAdded(Update):
    
    """
    Класс для обработки события добавления пользователя в чат.

    Attributes:
        inviter_id (Optional[int]): Идентификатор пользователя, добавившего нового участника. Может быть None.
        chat_id (Optional[int]): Идентификатор чата. Может быть None.
        user (User): Объект пользователя, добавленного в чат.
        bot (Optional[Bot]): Объект бота, исключается из сериализации.
    """
    
    inviter_id: Optional[int] = None
    chat_id: Optional[int] = None
    user: User
    bot: Optional[Any] = Field(default=None, exclude=True)
    
    if TYPE_CHECKING:
        bot: Optional[Bot]

    def get_ids(self):
        
        """
        Возвращает кортеж идентификаторов (chat_id, user_id).

        Returns:
            Tuple[Optional[int], Optional[int]]: Идентификаторы чата и пользователя.
        """
        
        return (self.chat_id, self.inviter_id)