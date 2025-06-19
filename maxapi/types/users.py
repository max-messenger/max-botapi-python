from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from ..enums.chat_permission import ChatPermission
from ..types.command import BotCommand


class User(BaseModel):
    user_id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_bot: bool
    last_activity_time: int
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    full_avatar_url: Optional[str] = None
    commands: Optional[List[BotCommand]] = None

    class Config:
        json_encoders = {
            datetime: lambda v: int(v.timestamp() * 1000)
        }


class ChatAdmin(BaseModel):
    user_id: int
    permissions: List[ChatPermission]