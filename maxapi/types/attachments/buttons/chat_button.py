from typing import Optional

from .button import Button


class ChatButton(Button):
    chat_title: Optional[str] = None
    chat_description: Optional[str] = None
    start_payload: Optional[str] = None
    chat_title: Optional[str] = None
    uuid: Optional[int] = None