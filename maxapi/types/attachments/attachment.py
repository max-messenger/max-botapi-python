from typing import List, Optional, Union
from pydantic import BaseModel

from ...types.attachments.upload import AttachmentUpload

from ...types.attachments.buttons import InlineButtonUnion
from ...types.users import User

from ...enums.attachment import AttachmentType


class StickerAttachmentPayload(BaseModel):
    
    """
    Данные для вложения типа стикер.

    Attributes:
        url (str): URL стикера.
        code (str): Код стикера.
    """
    
    url: str
    code: str


class PhotoAttachmentPayload(BaseModel):
    
    """
    Данные для фото-вложения.

    Attributes:
        photo_id (int): Идентификатор фотографии.
        token (str): Токен для доступа к фото.
        url (str): URL фотографии.
    """
    
    photo_id: int
    token: str
    url: str


class OtherAttachmentPayload(BaseModel):
    
    """
    Данные для общих типов вложений (файлы и т.п.).

    Attributes:
        url (str): URL вложения.
        token (Optional[str]): Опциональный токен доступа.
    """
    
    url: str
    token: Optional[str] = None


class ContactAttachmentPayload(BaseModel):
    
    """
    Данные для контакта.

    Attributes:
        vcf_info (Optional[str]): Информация в формате vcf.
        max_info (Optional[User]): Дополнительная информация о пользователе.
    """
    
    vcf_info: Optional[str] = None
    max_info: Optional[User] = None


class ButtonsPayload(BaseModel):
    
    """
    Данные для вложения с кнопками.

    Attributes:
        buttons (List[List[InlineButtonUnion]]): Двумерный список inline-кнопок.
    """
    
    buttons: List[List[InlineButtonUnion]]


class Attachment(BaseModel):
    
    """
    Универсальный класс вложения с типом и полезной нагрузкой.

    Attributes:
        type (AttachmentType): Тип вложения.
        payload (Optional[Union[...] ]): Полезная нагрузка, зависит от типа вложения.
    """
    
    type: AttachmentType
    payload: Optional[Union[
        AttachmentUpload,
        PhotoAttachmentPayload, 
        OtherAttachmentPayload, 
        ContactAttachmentPayload, 
        ButtonsPayload,
        StickerAttachmentPayload
    ]] = None

    class Config:
        use_enum_values = True