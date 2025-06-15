from enum import Enum

class ApiPath(str, Enum):
    ME = '/me'
    CHATS = '/chats'
    MESSAGES = '/messages'
    UPDATES = '/updates'