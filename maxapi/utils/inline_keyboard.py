from ..enums.attachment import AttachmentType
from ..types.attachments.attachment import Attachment, ButtonsPayload


class InlineKeyboardBuilder:
    def __init__(self):
        self.payload = []

    def row(self, *buttons):
        self.payload.append([*buttons])

    def as_markup(self):
        return Attachment(
            type=AttachmentType.INLINE_KEYBOARD,
            payload=ButtonsPayload(
                buttons=self.payload
            )
        )