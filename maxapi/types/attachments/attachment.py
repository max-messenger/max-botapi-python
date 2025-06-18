from typing import List, Optional, Union
from pydantic import BaseModel

from ...types.attachments.buttons import InlineButtonUnion
from ...types.users import User
from ...enums.attachment import AttachmentType

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
    buttons: List[List[InlineButtonUnion]]


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