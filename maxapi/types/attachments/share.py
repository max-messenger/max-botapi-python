from typing import Optional

from .attachment import Attachment


class Share(Attachment):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
