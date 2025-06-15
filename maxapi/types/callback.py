from typing import Optional
from pydantic import BaseModel

from ..types.users import User


class Callback(BaseModel):
    timestamp: int
    callback_id: str
    payload: Optional[str] = None
    user: User