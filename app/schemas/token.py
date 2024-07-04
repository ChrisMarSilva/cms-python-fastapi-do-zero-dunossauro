from pydantic import BaseModel


class Token(BaseModel):  # TokenRequest
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
