from typing import Optional

from . import Update
from ...types.users import User

class BotStarted(Update):
    chat_id: Optional[int] = None
    user: User
    user_locale: Optional[str] = None
    payload: Optional[str] = None