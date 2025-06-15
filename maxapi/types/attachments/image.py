from typing import Literal
from .attachment import Attachment


class Image(Attachment):
    type: Literal['image'] = 'image'