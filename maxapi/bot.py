from typing import Any, Dict, List

from .methods.edit_message import EditMessage
from .enums.parse_mode import ParseMode
from .types.attachments.attachment import Attachment
from .types.message import NewMessageLink
from .types.users import BotCommand
from .methods.change_info import ChangeInfo
from .methods.get_me import GetMe
from .methods.get_messages import GetMessages
from .methods.get_chats import GetChats
from .methods.send_message import SendMessage
from .connection.base import BaseConnection
    

class Bot(BaseConnection):

    def __init__(self, token: str):
        self.__token = token
        self.params = {
            'access_token': self.__token
        }
        
    async def send_message(
            self,
            chat_id: int = None, 
            user_id: int = None,
            disable_link_preview: bool = False,
            text: str = None,
            attachments: List[Attachment] = None,
            link: NewMessageLink = None,
            notify: bool = True,
            parse_mode: ParseMode = None
        ):
        return await SendMessage(
            bot=self,
            chat_id=chat_id,
            user_id=user_id,
            disable_link_preview=disable_link_preview,
            text=text,
            attachments=attachments,
            link=link,
            notify=notify,
            parse_mode=parse_mode
        ).request()
    
    async def edit_message(
            self,
            message_id: str,
            text: str = None,
            attachments: List[Attachment] = None,
            link: NewMessageLink = None,
            notify: bool = True,
            parse_mode: ParseMode = None
        ):
        return await EditMessage(
            bot=self,
            message_id=message_id,
            text=text,
            attachments=attachments,
            link=link,
            notify=notify,
            parse_mode=parse_mode
        ).request()

    async def get_messages(self, chat_id: int = None):
        return await GetMessages(self, chat_id).request()

    async def get_me(self):
        return await GetMe(self).request()
    
    async def change_info(
            self, 
            name: str = None, 
            description: str = None,
            commands: List[BotCommand] = None,
            photo: Dict[str, Any] = None
        ):

        return await ChangeInfo(
            bot=self, 
            name=name, 
            description=description, 
            commands=commands, 
            photo=photo
        ).request()
    
    async def get_chats(self):
        return await GetChats(self).request()