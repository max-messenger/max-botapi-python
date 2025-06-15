from typing import Optional

from . import Update
from ...types.users import User

class BotRemoved(Update):
    chat_id: Optional[int] = None
    user: User