from enum import Enum


class ChatStatus(str, Enum):
    ACTIVE = 'active'
    REMOVED = 'removed'
    LEFT = 'left'
    CLOSED = 'closed'
    SUSPENDED = 'suspended'