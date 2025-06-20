from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field

from .update import Update

from ...types.message import Message

if TYPE_CHECKING:
    from ...bot import Bot


class MessageEdited(Update):
    
    """
    Обновление, сигнализирующее об изменении сообщения.

    Attributes:
        message (Message): Объект измененного сообщения.
        bot (Optional[Any]): Экземпляр бота, не сериализуется.
    """
    
    message: Message
    bot: Optional[Any] = Field(default=None, exclude=True)
    
    if TYPE_CHECKING:
        bot: Optional[Bot]

    def get_ids(self):
        
        """
        Возвращает кортеж идентификаторов (chat_id, user_id).

        Returns:
            Tuple[Optional[int], Optional[int]]: Идентификаторы чата и пользователя.
        """
        
        return (self.message.recipient.chat_id, self.message.recipient.user_id)