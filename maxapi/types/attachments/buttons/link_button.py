from typing import Optional

from .button import Button


class LinkButton(Button):
    url: Optional[str] = None