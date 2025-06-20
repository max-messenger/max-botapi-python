from typing import Optional

from .button import Button


class ChatButton(Button):
    
    """
    Attributes:
        type: Тип кнопки (наследуется от Button)
        text: Текст кнопки (наследуется от Button)
        chat_title: Название чата (до 128 символов)
        chat_description: Описание чата (до 256 символов)
        start_payload: Данные, передаваемые при старте чата (до 512 символов)
        uuid: Уникальный идентификатор чата
    """
    
    chat_title: Optional[str] = None
    chat_description: Optional[str] = None
    start_payload: Optional[str] = None
    chat_title: Optional[str] = None
    uuid: Optional[int] = None