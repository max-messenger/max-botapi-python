from typing import Any
from pydantic import BaseModel

from ...types.message import Message


class SendedMessage(BaseModel):
    message: Message