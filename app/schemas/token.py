from pydantic import BaseModel


class TokenRequest(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
