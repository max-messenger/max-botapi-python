from typing import Any, Optional
from pydantic import BaseModel

from ...types.message import Message


class GettedUploadUrl(BaseModel):
    url: Optional[str] = None
    token: Optional[str] = None