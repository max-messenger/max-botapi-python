from . import Update
from ...types.message import Message


class MessageEdited(Update):
    message: Message