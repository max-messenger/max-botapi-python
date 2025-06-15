from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Optional, List, Union, TYPE_CHECKING

from ..enums.parse_mode import ParseMode
from ..types.attachments.attachment import Attachment
from ..types.attachments.share import Share
from .attachments.buttons.attachment_button import AttachmentButton
from ..enums.text_style import TextStyle
from ..enums.chat_type import ChatType
from ..enums.message_link_type import MessageLinkType
from .attachments.sticker import Sticker
from .attachments.file import File
from .attachments.image import Image
from .attachments.video import Video
from .attachments.audio import Audio
from ..types.users import User


if TYPE_CHECKING:
    from ..bot import Bot


class MarkupElement(BaseModel):
    type: TextStyle
    from_: int = Field(..., alias='from')
    length: int

    class Config:
        populate_by_name = True


class MarkupLink(MarkupElement):
    url: Optional[str] = None


class Recipient(BaseModel):
    user_id: Optional[int] = None  # Для пользователя
    chat_id: Optional[int] = None  # Для чата
    chat_type: ChatType  # Тип получателя (диалог или чат)


class MessageBody(BaseModel):
    mid: str
    seq: int
    text: str = None
    attachments: Optional[
        List[
            Union[
                AttachmentButton,
                Audio,
                Video,
                File,
                Image,
                Sticker,
                Share
            ]
        ]
    ] = []

    markup: Optional[
        List[
            Union[
                MarkupLink, MarkupElement
            ]
        ]
    ] = []


class MessageStat(BaseModel):
    views: int


class LinkedMessage(BaseModel):
    type: MessageLinkType
    sender: User
    chat_id: Optional[int] = None
    message: MessageBody


class Message(BaseModel):
    sender: User
    recipient: Recipient
    timestamp: int
    link: Optional[LinkedMessage] = None
    body: Optional[MessageBody] = None
    stat: Optional[MessageStat] = None
    url: Optional[str] = None
    bot: Optional[Any] = None

    async def answer(self,
            text: str = None,
            disable_link_preview: bool = False,
            attachments: List[Attachment] = None,
            link: NewMessageLink = None,
            notify: bool = True,
            parse_mode: ParseMode = None
        ):
        bot: Bot = self.bot
        return await bot.send_message(
            chat_id=self.recipient.chat_id,
            user_id=self.recipient.user_id,
            text=text,
            disable_link_preview=disable_link_preview,
            attachments=attachments,
            link=link,
            notify=notify,
            parse_mode=parse_mode
        )


class Messages(BaseModel):
    messages: List[Message]


class NewMessageLink(BaseModel):
    type: MessageLinkType
    mid: str