from typing import List, Optional
from pydantic import BaseModel

from ...types.chats import ChatMember


class GettedListAdminChat(BaseModel):
    members: List[ChatMember]
    marker: Optional[int] = None