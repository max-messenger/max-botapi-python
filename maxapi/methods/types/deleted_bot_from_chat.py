from typing import Optional
from pydantic import BaseModel


class DeletedBotFromChat(BaseModel):
    success: bool
    message: Optional[str] = None