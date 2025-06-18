from typing import Optional

from maxapi.enums.button_type import ButtonType

from ....enums.intent import Intent
from .button import Button


class CallbackButton(Button):
    type: ButtonType = ButtonType.CALLBACK
    payload: Optional[str] = None
    intent: Intent = Intent.DEFAULT