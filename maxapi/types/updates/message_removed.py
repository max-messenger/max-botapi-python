from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field

from .update import Update

if TYPE_CHECKING:
    from ...bot import Bot


class MessageRemoved(Update):
    message_id: Optional[str] = None
    chat_id: Optional[int] = None
    user_id: Optional[int] = None
    bot: Optional[Any] = Field(default=None, exclude=True)
    
    if TYPE_CHECKING:
        bot: Optional[Bot]

    def get_ids(self):
        return (self.chat_id, self.user_id)