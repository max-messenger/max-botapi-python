from typing import Optional
from pydantic import BaseModel


class SendedAction(BaseModel):
    success: bool
    message: Optional[str] = None