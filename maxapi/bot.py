from datetime import datetime
from typing import Any, Dict, List, TYPE_CHECKING

from .methods.get_upload_url import GetUploadURL
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
from .enums.upload_type import UploadType

from .types.attachments.attachment import Attachment
from .types.attachments.image import PhotoAttachmentRequestPayload
from .types.message import Messages, NewMessageLink
from .types.users import ChatAdmin, User
from .types.command import BotCommand

from .connection.base import BaseConnection

if TYPE_CHECKING:
    from .types.message import Message
    from .methods.types.added_admin_chat import AddedListAdminChat
    from .methods.types.added_members_chat import AddedMembersChat
    from .methods.types.deleted_bot_from_chat import DeletedBotFromChat
    from .methods.types.deleted_chat import DeletedChat
    from .methods.types.deleted_message import DeletedMessage
    from .methods.types.deleted_pin_message import DeletedPinMessage
    from .methods.types.edited_message import EditedMessage
    from .methods.types.getted_list_admin_chat import GettedListAdminChat
    from .methods.types.getted_members_chat import GettedMembersChat
    from .methods.types.getted_pineed_message import GettedPin
    from .methods.types.getted_upload_url import GettedUploadUrl
    from .methods.types.pinned_message import PinnedMessage
    from .methods.types.removed_admin import RemovedAdmin
    from .methods.types.removed_member_chat import RemovedMemberChat
    from .methods.types.sended_action import SendedAction
    from .methods.types.sended_callback import SendedCallback
    from .methods.types.sended_message import SendedMessage
    from maxapi.types.attachments.video import Video
    from maxapi.types.chats import Chat, ChatMember, Chats
    from maxapi.types.updates import UpdateUnion
    

class Bot(BaseConnection):
    
    """Основной класс для работы с API бота.

    Предоставляет методы для взаимодействия с чатами, сообщениями,
    пользователями и другими функциями бота.
    """

    def __init__(self, token: str):
        
        """Инициализирует экземпляр бота с указанным токеном.

        :param token: Токен доступа к API бота
        """
        
        super().__init__()

        self.bot = self

        self.__token = token
        self.params = {'access_token': self.__token}
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
        ) -> SendedMessage:
        
        """Отправляет сообщение в чат или пользователю.

        :param chat_id: ID чата для отправки (обязателен, если не указан user_id)
        :param user_id: ID пользователя для отправки (обязателен, если не указан chat_id)
        :param disable_link_preview: Отключить предпросмотр ссылок (по умолчанию False)
        :param text: Текст сообщения
        :param attachments: Список вложений к сообщению
        :param link: Данные ссылки сообщения
        :param notify: Отправлять уведомление получателю (по умолчанию True)
        :param parse_mode: Режим форматирования текста

        :return: Объект отправленного сообщения
        """
        
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
        ) -> SendedAction:
        
        """Отправляет действие в чат (например, "печатает").

        :param chat_id: ID чата для отправки действия
        :param action: Тип действия (по умолчанию SenderAction.TYPING_ON)

        :return: Результат отправки действия
        """
        
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
        ) -> EditedMessage:
        
        """Редактирует существующее сообщение.

        :param message_id: ID сообщения для редактирования
        :param text: Новый текст сообщения
        :param attachments: Новые вложения
        :param link: Новая ссылка сообщения
        :param notify: Уведомлять получателя об изменении (по умолчанию True)
        :param parse_mode: Режим форматирования текста

        :return: Объект отредактированного сообщения
        """
        
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
        ) -> DeletedMessage:
        
        """Удаляет сообщение.

        :param message_id: ID сообщения для удаления

        :return: Результат удаления сообщения
        """
        
        return await DeleteMessage(
            bot=self,
            message_id=message_id,
        ).request()
    
    async def delete_chat(
            self,
            chat_id: int
        ) -> DeletedChat:
        
        """Удаляет чат.

        :param chat_id: ID чата для удаления

        :return: Результат удаления чата
        """
        
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
        ) -> Messages:
        
        """Получает сообщения из чата.

        :param chat_id: ID чата (обязателен, если не указаны message_ids)
        :param message_ids: Список ID сообщений для получения
        :param from_time: Время начала периода (datetime или timestamp)
        :param to_time: Время конца периода (datetime или timestamp)
        :param count: Количество сообщений (по умолчанию 50)

        :return: Список сообщений
        """
        
        return await GetMessages(
            bot=self, 
            chat_id=chat_id,
            message_ids=message_ids,
            from_time=from_time,
            to_time=to_time,
            count=count
        ).request()
    
    async def get_message(
            self, 
            message_id: str
        ) -> Messages:
        
        """Получает одно сообщение по ID.

        :param message_id: ID сообщения

        :return: Объект сообщения
        """
        
        return await self.get_messages(
            message_ids=[message_id]
        )

    async def get_me(self) -> User:
        
        """Получает информацию о текущем боте.

        :return: Объект пользователя бота
        """
        
        return await GetMe(self).request()
    
    async def get_pin_message(
            self, 
            chat_id: int
        ) -> GettedPin:
        
        """Получает закрепленное сообщение в чате.

        :param chat_id: ID чата

        :return: Закрепленное сообщение
        """
        
        return await GetPinnedMessage(
            bot=self, 
            chat_id=chat_id
        ).request()
    
    async def change_info(
            self, 
            name: str = None, 
            description: str = None,
            commands: List[BotCommand] = None,
            photo: Dict[str, Any] = None
        ) -> User:
        
        """Изменяет информацию о боте.

        :param name: Новое имя бота
        :param description: Новое описание бота
        :param commands: Список команд бота
        :param photo: Данные фотографии бота

        :return: Обновленная информация о боте
        """

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
        ) -> Chats:
        
        """Получает список чатов бота.

        :param count: Количество чатов (по умолчанию 50)
        :param marker: Маркер для пагинации

        :return: Список чатов
        """
        
        return await GetChats(
            bot=self,
            count=count,
            marker=marker
        ).request()
    
    async def get_chat_by_link(
            self, 
            link: str
        ) -> Chat:
        
        """Получает чат по ссылке.

        :param link: Ссылка на чат

        :return: Объект чата
        """
        
        return await GetChatByLink(bot=self, link=link).request()
    
    async def get_chat_by_id(
            self, 
            id: int
        ) -> Chat:
        
        """Получает чат по ID.

        :param id: ID чата

        :return: Объект чата
        """
        
        return await GetChatById(bot=self, id=id).request()
    
    async def edit_chat(
            self,
            chat_id: int,
            icon: PhotoAttachmentRequestPayload = None,
            title: str = None,
            pin: str = None,
            notify: bool = True,
        ) -> Chat:
        
        """Редактирует параметры чата.

        :param chat_id: ID чата
        :param icon: Данные иконки чата
        :param title: Новый заголовок чата
        :param pin: ID сообщения для закрепления
        :param notify: Уведомлять участников (по умолчанию True)

        :return: Обновленный объект чата
        """
        
        return await EditChat(
            bot=self,
            chat_id=chat_id,
            icon=icon,
            title=title,
            pin=pin,
            notify=notify
        ).request()
    
    async def get_video(
            self, 
            video_token: str
        ) -> Video:
        
        """Получает видео по токену.

        :param video_token: Токен видео

        :return: Объект видео
        """
        
        return await GetVideo(
            bot=self, 
            video_token=video_token
        ).request()

    async def send_callback(
            self,
            callback_id: str,
            message: 'Message' = None,
            notification: str = None
        ) -> SendedCallback:
        
        """Отправляет callback ответ.

        :param callback_id: ID callback
        :param message: Сообщение для отправки
        :param notification: Текст уведомления

        :return: Результат отправки callback
        """
        
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
        ) -> PinnedMessage:
        
        """Закрепляет сообщение в чате.

        :param chat_id: ID чата
        :param message_id: ID сообщения
        :param notify: Уведомлять участников (по умолчанию True)

        :return: Закрепленное сообщение
        """
        
        return await PinMessage(
            bot=self,
            chat_id=chat_id,
            message_id=message_id,
            notify=notify
        ).request()
    
    async def delete_pin_message(
            self,
            chat_id: int,
        ) -> DeletedPinMessage:
        
        """Удаляет закрепленное сообщение в чате.

        :param chat_id: ID чата

        :return: Результат удаления
        """
        
        return await DeletePinMessage(
            bot=self,
            chat_id=chat_id,
        ).request()
    
    async def get_me_from_chat(
            self,
            chat_id: int,
        ) -> ChatMember:
        
        """Получает информацию о боте в конкретном чате.

        :param chat_id: ID чата

        :return: Информация о боте в чате
        """
        
        return await GetMeFromChat(
            bot=self,
            chat_id=chat_id,
        ).request()
    
    async def delete_me_from_chat(
            self,
            chat_id: int,
        ) -> DeletedBotFromChat:
        
        """Удаляет бота из чата.

        :param chat_id: ID чата

        :return: Результат удаления
        """
        
        return await DeleteMeFromMessage(
            bot=self,
            chat_id=chat_id,
        ).request()
    
    async def get_list_admin_chat(
            self,
            chat_id: int,
        ) -> GettedListAdminChat:
        
        """Получает список администраторов чата.

        :param chat_id: ID чата

        :return: Список администраторов
        """
        
        return await GetListAdminChat(
            bot=self,
            chat_id=chat_id,
        ).request()
    
    async def add_list_admin_chat(
            self,
            chat_id: int,
            admins: List[ChatAdmin],
            marker: int = None
        ) -> AddedListAdminChat:
        
        """Добавляет администраторов в чат.

        :param chat_id: ID чата
        :param admins: Список администраторов
        :param marker: Маркер для пагинации

        :return: Результат добавления
        """
        
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
        ) -> RemovedAdmin:
        
        """Удаляет администратора из чата.

        :param chat_id: ID чата
        :param user_id: ID пользователя

        :return: Результат удаления
        """
        
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
        ) -> GettedMembersChat:
        
        """Получает участников чата.

        :param chat_id: ID чата
        :param user_ids: Фильтр по ID пользователей
        :param marker: Маркер для пагинации
        :param count: Количество участников

        :return: Список участников
        """
        
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
        ) -> AddedMembersChat:
        
        """Добавляет участников в чат.

        :param chat_id: ID чата
        :param user_ids: Список ID пользователей

        :return: Результат добавления
        """
        
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
        ) -> RemovedMemberChat:
        
        """Исключает участника из чата.

        :param chat_id: ID чата
        :param user_id: ID пользователя
        :param block: Блокировать пользователя (по умолчанию False)

        :return: Результат исключения
        """
        
        return await RemoveMemberChat(
            bot=self,
            chat_id=chat_id,
            user_id=user_id,
            block=block,
        ).request()
    
    async def get_updates(
            self,
        ) -> UpdateUnion:
        
        """Получает обновления для бота.

        :return: Список обновлений
        """
        
        return await GetUpdates(
            bot=self,
        ).request()
    
    async def get_upload_url(
            self,
            type: UploadType
        ) -> GettedUploadUrl:
        
        """Получает URL для загрузки файлов.

        :param type: Тип загружаемого файла

        :return: URL для загрузки
        """
        
        return await GetUploadURL(
            bot=self,
            type=type
        ).request()
    
    async def set_my_commands(
            self,
            *commands: BotCommand
        ) -> User:
        
        """Устанавливает список команд бота.

        :param commands: Список команд

        :return: Обновленная информация о боте
        """
        
        return await ChangeInfo(
            bot=self,
            commands=list(commands)
        ).request()