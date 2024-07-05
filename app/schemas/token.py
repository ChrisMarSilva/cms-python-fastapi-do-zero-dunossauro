from pydantic import BaseModel


class TokenRequest(BaseModel):
    access_token: str
    token_type: str
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "name": "Foo",
    #             "description": "A very nice Item",
    #             "price": 16.25,
    #             "tax": 1.67,
    #         }
    #     }


class TokenData(BaseModel):
    username: str | None = None
