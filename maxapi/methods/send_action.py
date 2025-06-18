

from typing import List, TYPE_CHECKING

from maxapi.enums.sender_action import SenderAction
from maxapi.methods.types.sended_action import SendedAction

from .types.sended_message import SendedMessage
from ..types.message import NewMessageLink
from ..types.attachments.attachment import Attachment
from ..enums.parse_mode import ParseMode
from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath
from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class SendAction(BaseConnection):
    def __init__(
            self,
            bot: 'Bot',
            chat_id: int = None,
            action: SenderAction = SenderAction.TYPING_ON
        ):
            self.bot = bot
            self.chat_id = chat_id
            self.action = action

    async def request(self) -> SendedAction:
        json = {}

        json['action'] = self.action.value

        return await super().request(
            method=HTTPMethod.POST, 
            path=ApiPath.CHATS + '/' + str(self.chat_id) + ApiPath.ACTIONS,
            model=SendedAction,
            params=self.bot.params,
            json=json
        )