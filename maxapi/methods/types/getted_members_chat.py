from typing import List, Optional
from pydantic import BaseModel

from ...types.chats import ChatMember


class GettedMembersChat(BaseModel):
    members: List[ChatMember]
    marker: Optional[int] = None