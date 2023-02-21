from pydantic import BaseModel, Field


class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)


class UserSignUp(User):
    email: str
    password: str = Field(..., min_length=8, max_length=20)


class UserSignIn(User):
    password: str = Field(..., min_length=8, max_length=20)


class UserAccount(User):
    email: str
    credit: int
