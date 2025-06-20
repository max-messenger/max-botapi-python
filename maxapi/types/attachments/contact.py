from typing import Literal

from .attachment import Attachment


class Contact(Attachment):
    
    """
    Вложение с типом контакта.

    Attributes:
        type (Literal['contact']): Тип вложения, всегда 'contact'.
    """
    
    type: Literal['contact'] = 'contact'