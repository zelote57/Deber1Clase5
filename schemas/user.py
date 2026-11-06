from sqlmodel import Field, SQLModel


class UserCreate(SQLModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(max_length=255)
    password: str = Field(min_length=8)


class UserRead(SQLModel):
    id: int
    username: str
    email: str


class Token(SQLModel):
    access_token: str
    token_type: str
