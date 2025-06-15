from typing import Optional

from . import Update
from ...types.message import Message


class MessageCreated(Update):
    message: Message
    user_locale: Optional[str] = None