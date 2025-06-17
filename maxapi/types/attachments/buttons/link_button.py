from typing import Optional

from ....types.attachments.buttons import Button


class LinkButton(Button):
    url: Optional[str] = None