from typing import Optional

from .button import Button


class LinkButton(Button):
    
    """
    Кнопка с внешней ссылкой.
    
    Args:
        url: Ссылка для перехода (должна содержать http/https)
    """

    url: Optional[str] = None