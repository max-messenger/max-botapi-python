from typing import Literal, Optional

from .attachment import Attachment


class Audio(Attachment):
    type: Literal['audio'] = 'audio'
    transcription: Optional[str] = None