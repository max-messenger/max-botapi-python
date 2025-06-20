from typing import Literal, Optional

from .attachment import Attachment


class Location(Attachment):
    
    """
    Вложение с типом геолокации.

    Attributes:
        type (Literal['location']): Тип вложения, всегда 'location'.
        latitude (Optional[float]): Широта.
        longitude (Optional[float]): Долгота.
    """
    
    type: Literal['location'] = 'location'
    latitude: Optional[float] = None
    longitude: Optional[float] = None