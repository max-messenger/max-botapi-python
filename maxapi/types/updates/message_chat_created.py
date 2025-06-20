from typing import Optional

from ...types.chats import Chat

from .update import Update


class MessageChatCreated(Update):
    chat: Chat
    title: Optional[str] = None
    message_id: Optional[str] = None
    start_payload: Optional[str] = None
    
    def get_ids(self):
        return (self.chat.chat_id, self.chat.owner_id)