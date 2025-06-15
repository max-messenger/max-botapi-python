from typing import Optional

from . import Update
from ...types.users import User


class UserAdded(Update):
    inviter_id: Optional[int] = None
    chat_id: Optional[int] = None
    user: User
