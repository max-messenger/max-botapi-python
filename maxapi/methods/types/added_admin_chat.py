from typing import List, Optional
from pydantic import BaseModel

from ...types.chats import ChatMember


class AddedListAdminChat(BaseModel):
    success: bool
    message: Optional[str] = None