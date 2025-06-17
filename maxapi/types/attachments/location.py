from typing import Literal, Optional

from .attachment import Attachment


class Location(Attachment):
    type: Literal['location'] = 'location'
    latitude: Optional[float] = None
    longitude: Optional[float] = None