from pydantic import BaseModel

from ...enums.update import UpdateType


class Update(BaseModel):
    
    """
    Базовая модель обновления.

    Attributes:
        update_type (UpdateType): Тип обновления.
        timestamp (int): Временная метка обновления.
    """
    
    update_type: UpdateType
    timestamp: int

    class Config:
        arbitrary_types_allowed=True