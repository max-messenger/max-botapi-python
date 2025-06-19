

from pydantic import BaseModel

from ...enums.upload_type import UploadType


class AttachmentPayload(BaseModel):
    token: str


class AttachmentUpload(BaseModel):
    type: UploadType
    payload: AttachmentPayload