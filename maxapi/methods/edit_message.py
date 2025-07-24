from __future__ import annotations

from typing import Any, Dict, List, TYPE_CHECKING, Optional

from ..utils.message import process_input_media

from .types.edited_message import EditedMessage
from ..types.message import NewMessageLink
from ..types.attachments.attachment import Attachment

from ..enums.parse_mode import ParseMode
from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot
    from ..types.input_media import InputMedia, InputMediaBuffer


class EditMessage(BaseConnection):
    
    """
    Класс для редактирования существующего сообщения через API.

    Args:
        bot (Bot): Экземпляр бота для выполнения запроса.
        message_id (str): Идентификатор сообщения для редактирования.
        text (str, optional): Новый текст сообщения.
        attachments (List[Attachment | InputMedia | InputMediaBuffer], optional): Список вложений для сообщения.
        link (NewMessageLink, optional): Связь с другим сообщением (ответ или пересылка).
        notify (bool, optional): Отправлять ли уведомление о сообщении (по умолчанию True).
        parse_mode (ParseMode, optional): Формат разметки текста (markdown, html и т.д.).
    """
    
    def __init__(
            self,
            bot: Bot,
            message_id: str,
            text: Optional[str] = None,
            attachments: Optional[List[Attachment | InputMedia | InputMediaBuffer]] = None,
            link: Optional[NewMessageLink] = None,
            notify: Optional[bool] = None,
            parse_mode: Optional[ParseMode] = None
        ):
            self.bot = bot
            self.message_id = message_id
            self.text = text
            self.attachments = attachments
            self.link = link
            self.notify = notify
            self.parse_mode = parse_mode

    async def fetch(self) -> EditedMessage:
        
        """
        Выполняет PUT-запрос для обновления сообщения.

        Формирует тело запроса на основе переданных параметров и отправляет запрос к API.

        Returns:
            EditedMessage: Обновлённое сообщение.
        """
        
        assert self.bot is not None
        params = self.bot.params.copy()

        json: Dict[str, Any] = {}

        params['message_id'] = self.message_id

        if not self.text is None: json['text'] = self.text
        
        if self.attachments:
            
            for att in self.attachments:

                if isinstance(att, InputMedia) or isinstance(att, InputMediaBuffer):
                    input_media = await process_input_media(
                        base_connection=self,
                        bot=self.bot,
                        att=att
                    )
                    json['attachments'].append(
                        input_media.model_dump()
                    ) 
                else:
                    json['attachments'].append(att.model_dump()) 
                    
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