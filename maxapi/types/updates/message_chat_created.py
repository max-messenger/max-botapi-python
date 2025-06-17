from typing import Optional

from ...types.chats import Chat

from . import Update

class MessageChatCreated(Update):
    chat: Chat
    title: Optional[str] = None
    message_id: Optional[str] = None
    start_payload: Optional[str] = None