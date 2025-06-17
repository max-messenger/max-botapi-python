from typing import Optional
from pydantic import BaseModel


class EditedMessage(BaseModel):
    success: bool
    message: Optional[str] = None