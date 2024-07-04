from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):  # UserRequest
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):  # UserResponse
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):  # UsersResponse
    users: list[UserPublic]


class Token(BaseModel):  # TokenRequest
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
