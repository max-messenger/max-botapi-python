from typing import Optional
from pydantic import BaseModel


class DeletedMessage(BaseModel):
    success: bool
    message: Optional[str] = None