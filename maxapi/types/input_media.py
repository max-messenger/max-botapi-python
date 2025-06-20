import mimetypes

from ..enums.upload_type import UploadType


class InputMedia:
    
    """
    Класс для представления медиафайла.

    Attributes:
        path (str): Путь к файлу.
        type (UploadType): Тип файла, определенный на основе MIME-типа.
    """
    
    def __init__(self, path: str):
        
        """
        Инициализирует объект медиафайла.

        Args:
            path (str): Путь к файлу.
        """
        
        self.path = path
        self.type = self.__detect_file_type(path)

    def __detect_file_type(self, path: str) -> UploadType:
        
        """
        Определяет тип файла на основе его MIME-типа.

        Args:
            path (str): Путь к файлу.

        Returns:
            UploadType: Тип файла (VIDEO, IMAGE, AUDIO или FILE).
        """
        
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