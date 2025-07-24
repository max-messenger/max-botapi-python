from typing import Optional

from ...enums.attachment import AttachmentType

from .attachment import Attachment


class Share(Attachment):
    
    """
    Вложение с типом "share" (поделиться).

    Attributes:
        type (Literal['share']): Тип вложения, всегда 'share'.
        title (Optional[str]): Заголовок для шаринга.
        description (Optional[str]): Описание.
        image_url (Optional[str]): URL изображения для предпросмотра.
    """
    
    type: AttachmentType = AttachmentType.SHARE
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
