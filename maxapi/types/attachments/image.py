from typing import Literal, Optional

from pydantic import BaseModel
from .attachment import Attachment


class PhotoAttachmentRequestPayload(BaseModel):
    url: Optional[str] = None
    token: Optional[str] = None
    photos: Optional[str] = None


class Image(Attachment):
    type: Literal['image'] = 'image'