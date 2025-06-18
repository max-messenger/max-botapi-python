from typing import Optional
from pydantic import BaseModel


class PinnedMessage(BaseModel):
    success: bool
    message: Optional[str] = None