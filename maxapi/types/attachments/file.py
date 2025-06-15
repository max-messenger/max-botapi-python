from typing import Literal, Optional

from .attachment import Attachment


class File(Attachment):
    type: Literal['file'] = 'file'
    filename: Optional[str] = None
    size: Optional[int] = None