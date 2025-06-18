from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field

from ...types.chats import Chat

from .update import Update

if TYPE_CHECKING:
    from ...bot import Bot


class MessageChatCreated(Update):
    chat: Chat
    title: Optional[str] = None
    message_id: Optional[str] = None
    start_payload: Optional[str] = None
    bot: Optional[Any] = Field(default=None, exclude=True)
    
    if TYPE_CHECKING:
        bot: Optional[Bot]

    def get_ids(self):
        return (self.chat_id, 0)