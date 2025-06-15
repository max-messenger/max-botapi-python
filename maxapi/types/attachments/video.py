from typing import Literal, Optional
from pydantic import BaseModel

from .attachment import Attachment


class VideoThumbnail(BaseModel):
    url: str


class Video(Attachment):
    type: Literal['video'] = 'video'
    thumbnail: VideoThumbnail
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
