from enum import Enum


class ButtonType(str, Enum):
    REQUEST_CONTACT = 'request_contact'
    CALLBACK = 'callback'
    LINK = 'link'
    REQUEST_GEO_LOCATION = 'request_geo_location'
    CHAT = 'chat'
