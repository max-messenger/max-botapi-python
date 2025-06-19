from pydantic import BaseModel, field_validator
from typing import Dict, List, Optional
from datetime import datetime

from ..enums.chat_status import ChatStatus
from ..enums.chat_type import ChatType
from ..enums.chat_permission import ChatPermission

from ..types.users import User
from ..types.message import Message


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
    participants: Optional[Dict[str, datetime]] = None
    is_public: bool
    link: Optional[str] = None
    description: Optional[str] = None
    dialog_with_user: Optional[User] = None
    messages_count: Optional[int] = None
    chat_message_id: Optional[str] = None
    pinned_message: Optional[Message] = None

    @field_validator('participants', mode='before')
    @classmethod
    def convert_timestamps(cls, value: Dict[str, int]) -> Dict[str, datetime]:
        return {
            key: datetime.fromtimestamp(ts / 1000)
            for key, ts in value.items()
        }

    class Config:
        arbitrary_types_allowed=True


class Chats(BaseModel):
    chats: List[Chat] = []
    marker: Optional[int] = None


class ChatMember(User):
    last_access_time: Optional[int] = None
    is_owner: Optional[bool] = None
    is_admin: Optional[bool] = None
    join_time: Optional[int] = None
    permissions: Optional[List[ChatPermission]] = None