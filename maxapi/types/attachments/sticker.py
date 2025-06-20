from typing import Literal, Optional

from .attachment import Attachment


class Sticker(Attachment):
    
    """
    Вложение с типом стикера.

    Attributes:
        type (Literal['sticker']): Тип вложения, всегда 'sticker'.
        width (Optional[int]): Ширина стикера в пикселях.
        height (Optional[int]): Высота стикера в пикселях.
    """
    
    type: Literal['sticker'] = 'sticker'
    width: Optional[int] = None
    height: Optional[int] = None