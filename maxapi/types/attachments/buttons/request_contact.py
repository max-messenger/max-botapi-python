from typing import Optional

from ....enums.button_type import ButtonType

from .button import Button


class RequestContactButton(Button):
    
    """
    Кнопка с контактом
    
    Args:
        text: Текст кнопки
    """

    type: ButtonType = ButtonType.REQUEST_CONTACT
    text: str