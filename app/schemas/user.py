from pydantic import BaseModel, ConfigDict, EmailStr


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
