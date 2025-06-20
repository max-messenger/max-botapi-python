from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field

from .update import Update

from ...types.users import User

if TYPE_CHECKING:
    from ...bot import Bot
    

class BotRemoved(Update):
    
    """
    Обновление, сигнализирующее об удалении бота из чата.

    Attributes:
        chat_id (Optional[int]): Идентификатор чата, из которого удалён бот.
        user (User): Объект пользователя-бота.
        bot (Optional[Any]): Ссылка на экземпляр бота, не сериализуется.
    """
    
    chat_id: Optional[int] = None
    user: User
    bot: Optional[Any] = Field(default=None, exclude=True)
    
    if TYPE_CHECKING:
        bot: Optional[Bot]

    def get_ids(self):
        return (self.chat_id, self.user.user_id)