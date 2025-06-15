from typing import List, Optional, Union
from pydantic import BaseModel

from ...types.attachments.buttons.chat_button import ChatButton
from ...types.attachments.buttons.request_contact import RequestContact
from ...types.attachments.buttons.request_geo_location_button import RequestGeoLocationButton
from ...types.attachments.buttons.link_button import LinkButton
from ...types.users import User
from ...enums.attachment import AttachmentType
from .buttons.callback_button import CallbackButton

AttachmentUnion = []


class StickerAttachmentPayload(BaseModel):
    url: str
    code: str


class PhotoAttachmentPayload(BaseModel):
    photo_id: int
    token: str
    url: str


class OtherAttachmentPayload(BaseModel):
    url: str
    token: Optional[str] = None


class ContactAttachmentPayload(BaseModel):
    vcf_info: Optional[str] = None
    max_info: Optional[User] = None


class ButtonsPayload(BaseModel):
    buttons: List[List[
        Union[
            LinkButton,
            CallbackButton,
            RequestGeoLocationButton,
            RequestContact,
            ChatButton
        ]
    ]]


class Attachment(BaseModel):
    type: AttachmentType
    payload: Optional[Union[
        PhotoAttachmentPayload, 
        OtherAttachmentPayload, 
        ContactAttachmentPayload, 
        ButtonsPayload,
        StickerAttachmentPayload
    ]] = None

    class Config:
        use_enum_values = True