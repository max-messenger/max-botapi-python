from enum import Enum


class ChatType(str, Enum):
    DIALOG = 'dialog'
    CHAT = 'chat'