from pydantic import BaseModel


class Error(BaseModel):
    code: int
    raw: dict