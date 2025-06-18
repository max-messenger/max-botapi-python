from enum import Enum

class ApiPath(str, Enum):
    ME = '/me'
    CHATS = '/chats'
    MESSAGES = '/messages'
    UPDATES = '/updates'
    VIDEOS = '/videos'
    ANSWERS = '/answers'
    ACTIONS = '/actions'
    PIN = '/pin'
    MEMBERS = '/members'
    ADMINS = '/admins'