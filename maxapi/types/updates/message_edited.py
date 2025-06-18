from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field
from .update import Update
from ...types.message import Message

if TYPE_CHECKING:
    from ...bot import Bot


class MessageEdited(Update):
    message: Message
    bot: Optional[Any] = Field(default=None, exclude=True)
    
    if TYPE_CHECKING:
        bot: Optional[Bot]

    def get_ids(self):
        return (self.message.recipient.chat_id, self.message.recipient.user_id)