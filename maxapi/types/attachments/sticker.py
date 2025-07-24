from typing import Optional

from ...enums.attachment import AttachmentType

from .attachment import Attachment


class Sticker(Attachment):
    
    """
    Вложение с типом стикера.

    Attributes:
        type (Literal['sticker']): Тип вложения, всегда 'sticker'.
        width (Optional[int]): Ширина стикера в пикселях.
        height (Optional[int]): Высота стикера в пикселях.
    """
    
    type: AttachmentType = AttachmentType.STICKER
    width: Optional[int] = None
    height: Optional[int] = None