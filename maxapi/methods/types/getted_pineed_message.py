from typing import Optional
from pydantic import BaseModel

from ...types.message import Message


class GettedPin(BaseModel):
    message: Optional[Message] = None