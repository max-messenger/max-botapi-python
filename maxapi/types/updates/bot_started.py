from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field

from .update import Update
from ...types.users import User

if TYPE_CHECKING:
    from ...bot import Bot


class BotStarted(Update):
    
    """
    Обновление, сигнализирующее о первом старте бота.

    Attributes:
        chat_id (Optional[int]): Идентификатор чата.
        user (User): Пользователь (бот).
        user_locale (Optional[str]): Локаль пользователя.
        payload (Optional[str]): Дополнительные данные.
        bot (Optional[Any]): Ссылка на экземпляр бота, не сериализуется.
    """
    
    chat_id: Optional[int] = None
    user: User
    user_locale: Optional[str] = None
    payload: Optional[str] = None
    bot: Optional[Any] = Field(default=None, exclude=True)
    
    if TYPE_CHECKING:
        bot: Optional[Bot]

    def get_ids(self):
        return (self.chat_id, self.user.user_id)