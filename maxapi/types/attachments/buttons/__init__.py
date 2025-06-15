from typing import Literal
from pydantic import BaseModel

from ....enums.button_type import ButtonType


class Button(BaseModel):
    type: ButtonType
    text: str

    class Config:
        use_enum_values = True