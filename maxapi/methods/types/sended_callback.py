from typing import TYPE_CHECKING, Any, Optional
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from ...bot import Bot


class SendedCallback(BaseModel):
    success: bool
    message: Optional[str] = None
    bot: Optional[Any] = Field(default=None, exclude=True)
    
    if TYPE_CHECKING:
        bot: Optional[Bot]
