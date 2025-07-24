from typing import TYPE_CHECKING

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class DownloadMedia(BaseConnection):
    
    """
    Класс для скачивания медиафайлов.

    Args:
        bot (Bot): Экземпляр бота для выполнения запроса.
        media_url (str): Ссылка на медиа.
        media_token (str): Токен медиа.
    """
    
    def __init__(
            self,
            bot: 'Bot',
            path: str,
            media_url: str,
            media_token: str
        ):
            self.bot = bot
            self.path = path
            self.media_url = media_url
            self.media_token = media_token

    async def fetch(self) -> int:
        
        """
        Выполняет GET-запрос для скачивания медиафайла

        Returns:
            int: Код операции.
        """
        
        return await super().download_file(
            path=self.path,
            url=self.media_url,
            token=self.media_token
        )