from typing import Optional
from pydantic import BaseModel


class Command:
    
    """
    Класс для представления команды бота.

    Attributes:
        text (str): Текст команды без префикса.
        prefix (str): Префикс команды. По умолчанию '/'.
    """
    
    def __init__(self, text: str, prefix: str = '/'):
        self.text = text
        self.prefix = prefix

    @property
    def command(self):
        
        """
        Возвращает полную команду с префиксом.

        Returns:
            str: Команда, состоящая из префикса и текста.
        """
        
        return self.prefix + self.text
    

class BotCommand(BaseModel):
    
    """
    Модель команды бота для сериализации.

    Attributes:
        name (str): Название команды.
        description (Optional[str]): Описание команды. Может быть None.
    """

    name: str
    description: Optional[str] = None
    
    
class CommandStart(Command):
    
    """
    Класс для представления команды /start бота.

    Attributes:
        prefix (str): Префикс команды. По умолчанию '/'.
    """
    
    text = 'start'
    
    def __init__(self, prefix: str = '/'):
        self.prefix = prefix