from typing import Literal, Optional

from .attachment import Attachment


class Sticker(Attachment):
    type: Literal['sticker'] = 'sticker'
    width: Optional[int] = None
    height: Optional[int] = None