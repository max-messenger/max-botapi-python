from typing import Optional
from pydantic import BaseModel


class DeletedPinMessage(BaseModel):
    success: bool
    message: Optional[str] = None