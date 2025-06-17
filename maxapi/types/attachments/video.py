from typing import TYPE_CHECKING, Any, Literal, Optional
from pydantic import BaseModel, Field

from .attachment import Attachment

if TYPE_CHECKING:
    from ...bot import Bot


class VideoUrl(BaseModel):
    mp4_1080: Optional[str] = None
    mp4_720: Optional[str] = None
    mp4_480: Optional[str] = None
    mp4_360: Optional[str] = None
    mp4_240: Optional[str] = None
    mp4_144: Optional[str] = None
    hls: Optional[str] = None


class VideoThumbnail(BaseModel):
    url: str


class Video(Attachment):
    type: Optional[Literal['video']] = 'video'
    token: Optional[str] = None
    urls: Optional[VideoUrl] = None
    thumbnail: VideoThumbnail
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    bot: Optional[Any] = Field(default=None, exclude=True)
    
    if TYPE_CHECKING:
        bot: Optional['Bot']
