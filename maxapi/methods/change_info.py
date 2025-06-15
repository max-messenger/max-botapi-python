

from typing import Any, Dict, List, TYPE_CHECKING

from ..types.users import BotCommand, User

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class ChangeInfo(BaseConnection):
    def __init__(
            self,
            bot: 'Bot',
            name: str = None, 
            description: str = None,
            commands: List[BotCommand] = None,
            photo: Dict[str, Any] = None
        ):
            self.bot = bot
            self.name = name
            self.description = description
            self.commands = commands
            self.photo = photo

    async def request(self) -> User:
        json = {}

        if self.name: json['name'] = self.name
        if self.description: json['description'] = self.description
        if self.commands: json['commands'] = [command.model_dump() for command in self.commands]
        if self.photo: json['photo'] = self.photo

        return await super().request(
            method=HTTPMethod.PATCH, 
            path=ApiPath.ME,
            model=User,
            params=self.bot.params,
            json=json
        )