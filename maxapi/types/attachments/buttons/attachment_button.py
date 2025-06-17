from typing import Literal
from pydantic import BaseModel

from ..attachment import ButtonsPayload


class AttachmentButton(BaseModel):
    type: Literal['inline_keyboard'] = 'inline_keyboard'
    payload: ButtonsPayload