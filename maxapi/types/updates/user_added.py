from typing import Optional

from .update import Update

from ...types.users import User


class UserAdded(Update):
    
    """
    Класс для обработки события добавления пользователя в чат.

    Attributes:
        inviter_id (Optional[int]): Идентификатор пользователя, добавившего нового участника. Может быть None.
        chat_id (Optional[int]): Идентификатор чата. Может быть None.
        user (User): Объект пользователя, добавленного в чат.
    """
    
    inviter_id: Optional[int] = None
    chat_id: Optional[int] = None
    user: User
    
    def get_ids(self):
        
        """
        Возвращает кортеж идентификаторов (chat_id, user_id).

        Returns:
            Tuple[Optional[int], Optional[int]]: Идентификаторы чата и пользователя.
        """
        
        return (self.chat_id, self.inviter_id)