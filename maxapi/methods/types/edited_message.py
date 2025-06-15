from pydantic import BaseModel

from ...types.message import Message


class EditedMessage(BaseModel):
    message: Message