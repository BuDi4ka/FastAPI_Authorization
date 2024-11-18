import datetime
from datetime import date
from pydantic import BaseModel, EmailStr, Field



class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"

class ContactModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    mobile_number: str
    date_of_birth: date
    additional_notes: str | None = None

class ContactResponseModel(BaseModel):
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"