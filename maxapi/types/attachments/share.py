from typing import Literal, Optional

from .attachment import Attachment


class Share(Attachment):
    type: Literal['share'] = 'share'
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
