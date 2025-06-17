from pydantic import BaseModel

from ...enums.update import UpdateType


class Update(BaseModel):
    update_type: UpdateType
    timestamp: int

    class Config:
        arbitrary_types_allowed=True