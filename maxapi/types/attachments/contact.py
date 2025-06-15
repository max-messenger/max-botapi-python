from typing import Literal

from .attachment import Attachment


class Contact(Attachment):
    type: Literal['contact'] = 'contact'