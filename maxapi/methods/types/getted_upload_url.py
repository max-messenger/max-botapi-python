from typing import Optional
from pydantic import BaseModel


class GettedUploadUrl(BaseModel):
    url: Optional[str] = None
    token: Optional[str] = None