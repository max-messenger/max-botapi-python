from __future__ import annotations
from typing import Any, Optional, TYPE_CHECKING

from pydantic import Field

from .update import Update

from ...types.message import Message

if TYPE_CHECKING:
    from ...bot import Bot


class MessageCreated(Update):
    
    """
    Обновление, сигнализирующее о создании нового сообщения.

    Attributes:
        message (Message): Объект сообщения.
        user_locale (Optional[str]): Локаль пользователя.
        bot (Optional[Any]): Экземпляр бота, не сериализуется.
    """
    
    message: Message
    user_locale: Optional[str] = None
    bot: Optional[Any] = Field(default=None, exclude=True)
    
    if TYPE_CHECKING:
        bot: Optional[Bot]

    def get_ids(self):
        
        """
        Возвращает кортеж идентификаторов (chat_id, user_id).

        Returns:
            tuple[Optional[int], int]: Идентификатор чата и пользователя.
        """
        
        return (self.message.recipient.chat_id, self.message.sender.user_id)