from typing import Optional

from . import Update
from ...types.users import User

class ChatTitleChanged(Update):
    chat_id: Optional[int] = None
    user: User
    title: Optional[str] = None