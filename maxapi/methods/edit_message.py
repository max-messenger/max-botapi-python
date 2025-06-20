from typing import List, TYPE_CHECKING

from .types.edited_message import EditedMessage
from ..types.message import NewMessageLink
from ..types.attachments.attachment import Attachment

from ..enums.parse_mode import ParseMode
from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class EditMessage(BaseConnection):
    
    """
    Класс для редактирования существующего сообщения через API.

    Args:
        bot (Bot): Экземпляр бота для выполнения запроса.
        message_id (str): Идентификатор сообщения для редактирования.
        text (str, optional): Новый текст сообщения.
        attachments (List[Attachment], optional): Список вложений для сообщения.
        link (NewMessageLink, optional): Связь с другим сообщением (ответ или пересылка).
        notify (bool, optional): Отправлять ли уведомление о сообщении (по умолчанию True).
        parse_mode (ParseMode, optional): Формат разметки текста (markdown, html и т.д.).
    """
    
    def __init__(
            self,
            bot: 'Bot',
            message_id: str,
            text: str = None,
            attachments: List['Attachment'] = None,
            link: 'NewMessageLink' = None,
            notify: bool = True,
            parse_mode: ParseMode = None
        ):
            self.bot = bot
            self.message_id = message_id
            self.text = text
            self.attachments = attachments
            self.link = link
            self.notify = notify
            self.parse_mode = parse_mode

    async def request(self) -> EditedMessage:
        
        """
        Выполняет PUT-запрос для обновления сообщения.

        Формирует тело запроса на основе переданных параметров и отправляет запрос к API.

        Returns:
            EditedMessage: Обновлённое сообщение.
        """
        
        params = self.bot.params.copy()

        json = {}

        params['message_id'] = self.message_id

        if not self.text is None: json['text'] = self.text
        if self.attachments: json['attachments'] = \
          [att.model_dump() for att in self.attachments]
        if not self.link is None: json['link'] = self.link.model_dump()
        if not self.notify is None: json['notify'] = self.notify
        if not self.parse_mode is None: json['format'] = self.parse_mode.value

        return await super().request(
            method=HTTPMethod.PUT, 
            path=ApiPath.MESSAGES,
            model=EditedMessage,
            params=params,
            json=json
        )