from datetime import datetime
from typing import Any, Dict, List, TYPE_CHECKING

from .methods.get_updates import GetUpdates
from .methods.remove_member_chat import RemoveMemberChat
from .methods.add_admin_chat import AddAdminChat
from .methods.add_members_chat import AddMembersChat
from .methods.get_members_chat import GetMembersChat
from .methods.remove_admin import RemoveAdmin
from .methods.get_list_admin_chat import GetListAdminChat
from .methods.delete_bot_from_chat import DeleteMeFromMessage
from .methods.get_me_from_chat import GetMeFromChat
from .methods.delete_pin_message import DeletePinMessage
from .methods.get_pinned_message import GetPinnedMessage
from .methods.pin_message import PinMessage
from .methods.delete_chat import DeleteChat
from .methods.send_action import SendAction
from .methods.edit_chat import EditChat
from .methods.get_chat_by_id import GetChatById
from .methods.get_chat_by_link import GetChatByLink
from .methods.send_callback import SendCallback
from .methods.get_video import GetVideo
from .methods.delete_message import DeleteMessage
from .methods.edit_message import EditMessage
from .methods.change_info import ChangeInfo
from .methods.get_me import GetMe
from .methods.get_messages import GetMessages
from .methods.get_chats import GetChats
from .methods.send_message import SendMessage

from .enums.parse_mode import ParseMode
from .enums.sender_action import SenderAction

from .types.attachments.attachment import Attachment
from .types.attachments.image import PhotoAttachmentRequestPayload
from .types.message import NewMessageLink
from .types.users import BotCommand, ChatAdmin

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
        self.marker_updates = None
        
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
    
    async def send_action(
            self,
            chat_id: int = None,
            action: SenderAction = SenderAction.TYPING_ON
        ):
        return await SendAction(
            bot=self,
            chat_id=chat_id,
            action=action
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
    
    async def delete_chat(
            self,
            chat_id: int
        ):
        return await DeleteChat(
            bot=self,
            chat_id=chat_id,
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
    
    async def get_pin_message(self, chat_id: int):
        return await GetPinnedMessage(bot=self, chat_id=chat_id).request()
    
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
    
    async def get_chats(
            self,
            count: int = 50,
            marker: int = None
        ):
        return await GetChats(
            bot=self,
            count=count,
            marker=marker
        ).request()
    
    async def get_chat_by_link(self, link: str):
        """под вопросом"""
        return await GetChatByLink(bot=self, link=link).request()
    
    async def get_chat_by_id(self, id: int):
        return await GetChatById(bot=self, id=id).request()
    
    async def edit_chat(
            self,
            chat_id: int,
            icon: PhotoAttachmentRequestPayload = None,
            title: str = None,
            pin: str = None,
            notify: bool = True,
    ):
        return await EditChat(
            bot=self,
            chat_id=chat_id,
            icon=icon,
            title=title,
            pin=pin,
            notify=notify
        ).request()
    
    async def get_video(self, video_token: str):
        return await GetVideo(bot=self, video_token=video_token).request()

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
    
    async def pin_message(
            self,
            chat_id: int,
            message_id: str,
            notify: bool = True
    ):
        return await PinMessage(
            bot=self,
            chat_id=chat_id,
            message_id=message_id,
            notify=notify
        ).request()
    
    async def delete_pin_message(
            self,
            chat_id: int,
    ):
        return await DeletePinMessage(
            bot=self,
            chat_id=chat_id,
        ).request()
    
    async def get_me_from_chat(
            self,
            chat_id: int,
    ):
        return await GetMeFromChat(
            bot=self,
            chat_id=chat_id,
        ).request()
    
    async def delete_me_from_chat(
            self,
            chat_id: int,
    ):
        return await DeleteMeFromMessage(
            bot=self,
            chat_id=chat_id,
        ).request()
    
    async def get_list_admin_chat(
            self,
            chat_id: int,
    ):
        return await GetListAdminChat(
            bot=self,
            chat_id=chat_id,
        ).request()
    
    async def add_list_admin_chat(
            self,
            chat_id: int,
            admins: List[ChatAdmin],
            marker: int = None
    ):
        return await AddAdminChat(
            bot=self,
            chat_id=chat_id,
            admins=admins,
            marker=marker,
        ).request()
    
    async def remove_admin(
            self,
            chat_id: int,
            user_id: int
    ):
        return await RemoveAdmin(
            bot=self,
            chat_id=chat_id,
            user_id=user_id,
        ).request()
    
    async def get_chat_members(
            self,
            chat_id: int,
            user_ids: List[int] = None,
            marker: int = None,
            count: int = None,
    ):
        return await GetMembersChat(
            bot=self,
            chat_id=chat_id,
            user_ids=user_ids,
            marker=marker,
            count=count,
        ).request()
    
    async def add_chat_members(
            self,
            chat_id: int,
            user_ids: List[str],
    ):
        return await AddMembersChat(
            bot=self,
            chat_id=chat_id,
            user_ids=user_ids,
        ).request()
    
    async def kick_chat_member(
            self,
            chat_id: int,
            user_id: int,
            block: bool = False,
    ):
        return await RemoveMemberChat(
            bot=self,
            chat_id=chat_id,
            user_id=user_id,
            block=block,
        ).request()
    
    async def get_updates(
            self,
    ):
        return await GetUpdates(
            bot=self,
        ).request()