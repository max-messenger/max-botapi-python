from typing import Optional

from ....enums.intent import Intent
from . import Button


class CallbackButton(Button):
    payload: Optional[str] = None
    intent: Intent