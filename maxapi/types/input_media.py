import mimetypes

from ..enums.upload_type import UploadType


class InputMedia:
    def __init__(self, path: str):
        self.path = path
        self.type = self.__detect_file_type(path)

    def __detect_file_type(self, path: str) -> UploadType:
        mime_type, _ = mimetypes.guess_type(path)

        if mime_type is None:
            return UploadType.FILE

        if mime_type.startswith('video/'):
            return UploadType.VIDEO
        elif mime_type.startswith('image/'):
            return UploadType.IMAGE
        elif mime_type.startswith('audio/'):
            return UploadType.AUDIO
        else:
            return UploadType.FILE