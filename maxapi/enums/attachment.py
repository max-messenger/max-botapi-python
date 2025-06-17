from enum import Enum

class AttachmentType(str, Enum):
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'
    FILE = 'file'
    STICKER = 'sticker'
    CONTACT = 'contact'
    INLINE_KEYBOARD = 'inline_keyboard'
    LOCATION = 'location'