from typing import List, Optional
from pydantic import BaseModel


class RemovedAdmin(BaseModel):
    success: bool
    message: Optional[str] = None