from enum import Enum


class UploadType(str, Enum):
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'
    FILE = 'file'