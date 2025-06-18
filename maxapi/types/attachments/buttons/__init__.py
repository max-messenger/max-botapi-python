from typing import Union

from .callback_button import CallbackButton
from .chat_button import ChatButton
from .link_button import LinkButton
from .request_contact import RequestContact
from .request_geo_location_button import RequestGeoLocationButton

InlineButtonUnion = Union[
    CallbackButton,
    ChatButton,
    LinkButton,
    RequestContact,
    RequestGeoLocationButton
]