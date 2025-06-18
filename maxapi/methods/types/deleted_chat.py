from typing import Optional
from pydantic import BaseModel


class DeletedChat(BaseModel):
    success: bool
    message: Optional[str] = None