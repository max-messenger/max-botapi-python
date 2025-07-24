from typing import Optional

from ...enums.attachment import AttachmentType

from .attachment import Attachment


class Audio(Attachment):
    
    """
    Вложение с типом аудио.

    Attributes:
        type (Literal['audio']): Тип вложения, всегда 'audio'.
        transcription (Optional[str]): Транскрипция аудио (если есть).
    """
    
    type: AttachmentType = AttachmentType.AUDIO
    transcription: Optional[str] = None