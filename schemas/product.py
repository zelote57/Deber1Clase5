from sqlmodel import Field, SQLModel


class ProductCreate(SQLModel):
    name: str = Field(min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=300)
    price: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)


class ProductUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=300)
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)


class ProductRead(SQLModel):
    id: int
    name: str
    description: str | None
    price: float
    stock: int
    user_id: int
