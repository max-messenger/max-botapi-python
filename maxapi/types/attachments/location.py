from typing import Optional

from ...enums.attachment import AttachmentType

from .attachment import Attachment


class Location(Attachment):
    
    """
    Вложение с типом геолокации.

    Attributes:
        type (Literal['location']): Тип вложения, всегда 'location'.
        latitude (Optional[float]): Широта.
        longitude (Optional[float]): Долгота.
    """
    
    type: AttachmentType = AttachmentType.LOCATION
    latitude: Optional[float] = None
    longitude: Optional[float] = None