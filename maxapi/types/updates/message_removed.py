from typing import Optional

from .update import Update


class MessageRemoved(Update):
    
    """
    Класс для обработки события удаления сообщения в чате.

    Attributes:
        message_id (Optional[str]): Идентификатор удаленного сообщения. Может быть None.
        chat_id (Optional[int]): Идентификатор чата. Может быть None.
        user_id (Optional[int]): Идентификатор пользователя. Может быть None.
    """
    
    message_id: Optional[str] = None
    chat_id: Optional[int] = None
    user_id: Optional[int] = None

    def get_ids(self):
        
        """
        Возвращает кортеж идентификаторов (chat_id, user_id).

        Returns:
            Tuple[Optional[int], Optional[int]]: Идентификаторы чата и пользователя.
        """
        
        return (self.chat_id, self.user_id)