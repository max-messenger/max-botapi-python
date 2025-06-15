from typing import Optional

from . import Update
from ...types.callback import Callback
from ...types.message import Message


class MessageCallback(Update):
    message: Message
    user_locale: Optional[str] = None
    callback: Callback