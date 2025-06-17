from pydantic import BaseModel


class Error(BaseModel):
    code: int
    text: str