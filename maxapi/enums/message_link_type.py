from enum import Enum


class MessageLinkType(str, Enum):
    FORWARD = 'forward'
    REPLY = 'reply'