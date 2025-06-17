from typing import Optional

from . import Update


class MessageRemoved(Update):
    message_id: Optional[str] = None
    chat_id: Optional[int] = None
    user_id: Optional[int] = None