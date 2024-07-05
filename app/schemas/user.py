from pydantic import BaseModel, ConfigDict, EmailStr

# from typing import Any, List, Optional


class UserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)
    #
    # class Config:
    #     orm_mode = True


class UsersResponse(BaseModel):
    users: list[UserResponse]
    #  users = List[UserPublic] = []
    # complemento: Optional[str] = None
