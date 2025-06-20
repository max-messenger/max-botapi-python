from typing import Literal
from pydantic import BaseModel

from ..attachment import ButtonsPayload


class AttachmentButton(BaseModel):
    
    """
    Модель кнопки вложения для сообщения.

    Attributes:
        type: Тип кнопки, фиксированное значение 'inline_keyboard'
        payload: Полезная нагрузка кнопки (массив рядов кнопок)
    """
    
    type: Literal['inline_keyboard'] = 'inline_keyboard'
    payload: ButtonsPayload