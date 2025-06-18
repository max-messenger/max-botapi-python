from typing import Any, List, Optional, TYPE_CHECKING, Union

from pydantic import BaseModel, Field

from .update import Update
from ...types.callback import Callback
from ...types.message import Message

from ...enums.parse_mode import ParseMode
from ...types.message import NewMessageLink
from ...types.attachments.share import Share
from ..attachments.buttons.attachment_button import AttachmentButton
from ..attachments.sticker import Sticker
from ..attachments.file import File
from ..attachments.image import Image
from ..attachments.video import Video
from ..attachments.audio import Audio


if TYPE_CHECKING:
    from ...bot import Bot


class MessageForCallback(BaseModel):
    text: Optional[str] = None
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
    link: Optional[NewMessageLink] = None
    notify: Optional[bool] = True
    format: Optional[ParseMode] = None


class MessageCallback(Update):
    message: Message
    user_locale: Optional[str] = None
    callback: Callback
    bot: Optional[Any] = Field(default=None, exclude=True)

    if TYPE_CHECKING:
        bot: Optional[Bot]

    def get_ids(self):
        return (self.message.recipient.chat_id, self.message.recipient.user_id)
    
    async def answer(
            self,
            notification: str,
            new_text: str = None,
            link: NewMessageLink = None,
            notify: bool = True,
            format: ParseMode = None,
        ):
        message = MessageForCallback()

        message.text = new_text
        message.attachments = self.message.body.attachments
        message.link = link
        message.notify = notify
        message.format = format

        return await self.bot.send_callback(
            callback_id=self.callback.callback_id,
            message=message,
            notification=notification
        )