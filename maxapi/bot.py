from datetime import datetime
from typing import Any, Dict, List, TYPE_CHECKING

from .methods.send_callback import SendCallback

from .methods.get_video import GetVideo

from .methods.delete_message import DeleteMessage
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

if TYPE_CHECKING:
    from .types.message import Message
    

class Bot(BaseConnection):

    def __init__(self, token: str):
        super().__init__()
        self.bot = self

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
    
    async def delete_message(
            self,
            message_id: str
        ):
        return await DeleteMessage(
            bot=self,
            message_id=message_id,
        ).request()

    async def get_messages(
            self, 
            chat_id: int = None,
            message_ids: List[str] = None,
            from_time: datetime | int = None,
            to_time: datetime | int = None,
            count: int = 50,
        ):
        return await GetMessages(
            bot=self, 
            chat_id=chat_id,
            message_ids=message_ids,
            from_time=from_time,
            to_time=to_time,
            count=count
        ).request()
    
    async def get_message(self, message_id: str):
        return await self.get_messages(message_ids=[message_id])

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
    
    async def get_video(self, video_token: str):
        return await GetVideo(self, video_token).request()

    async def send_callback(
            self,
            callback_id: str,
            message: 'Message' = None,
            notification: str = None
    ):
        return await SendCallback(
            bot=self,
            callback_id=callback_id,
            message=message,
            notification=notification
        ).request()