from pydantic import BaseModel


class Error(BaseModel):
    
    """
    Модель ошибки.

    Attributes:
        code (int): Код ошибки.
        raw (dict): Необработанные данные ошибки.
    """
    
    code: int
    raw: dict