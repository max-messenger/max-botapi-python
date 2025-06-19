from __future__ import annotations
from typing import Any, Optional, TYPE_CHECKING, ForwardRef

from pydantic import Field

from .update import Update
from ...types.message import Message

if TYPE_CHECKING:
    from ...bot import Bot


class MessageCreated(Update):
    message: Message
    user_locale: Optional[str] = None
    bot: Optional[Any] = Field(default=None, exclude=True)
    
    if TYPE_CHECKING:
        bot: Optional[Bot]

    def get_ids(self):
        return (self.message.recipient.chat_id, self.message.sender.user_id)