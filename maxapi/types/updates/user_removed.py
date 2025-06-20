from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field

from .update import Update

from ...types.users import User

if TYPE_CHECKING:
    from ...bot import Bot


class UserRemoved(Update):
    
    """
    Класс для обработки события удаления пользователя из чата.

    Attributes:
        admin_id (Optional[int]): Идентификатор администратора, удалившего пользователя. Может быть None.
        chat_id (Optional[int]): Идентификатор чата. Может быть None.
        user (User): Объект пользователя, удаленного из чата.
        bot (Optional[Bot]): Объект бота, исключается из сериализации.
    """
    
    admin_id: Optional[int] = None
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
        
        return (self.chat_id, self.admin_id)