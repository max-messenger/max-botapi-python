from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime

from ..types.users import User
from ..types.message import Message

class ChatType(str, Enum):
    DIALOG = "dialog"
    CHAT = "chat"

class ChatStatus(str, Enum):
    ACTIVE = "active"
    REMOVED = "removed"
    LEFT = "left"
    CLOSED = "closed"
    SUSPENDED = "suspended"

class Icon(BaseModel):
    url: str

class Chat(BaseModel):
    chat_id: int
    type: ChatType
    status: ChatStatus
    title: Optional[str] = None
    icon: Optional[Icon] = None
    last_event_time: int
    participants_count: int
    owner_id: Optional[int] = None
    participants: None = None
    is_public: bool
    link: Optional[str] = None
    description: Optional[str] = None
    dialog_with_user: Optional[User] = None
    messages_count: Optional[int] = None
    chat_message_id: Optional[str] = None
    pinned_message: Optional[Message] = None

    class Config:
        arbitrary_types_allowed=True


class Chats(BaseModel):
    chats: List[Chat] = []