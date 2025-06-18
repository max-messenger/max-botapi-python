from enum import Enum

class SenderAction(str, Enum):
    TYPING_ON = 'typing_on'
    SENDING_PHOTO = 'sending_photo'
    SENDING_VIDEO = 'sending_video'
    SENDING_AUDIO = 'sending_audio'
    SENDING_FILE = 'sending_file'
    MARK_SEEN = 'mark_seen'