from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, SecretStr


class UserIn(BaseModel):
    first_name: str = Field(max_length=32)
    last_name: str = Field(max_length=32)
    email: EmailStr = Field(max_length=128)
    password: SecretStr = Field(max_length=64)


class User(UserIn):
    id: int


class ProductIn(BaseModel):
    title: str = Field(max_length=32)
    description: str
    price: float


class Product(ProductIn):
    id: int


class OrderIn(BaseModel):
    user_id: int = Field(...)
    product_id: int = Field(...)
    order_date: datetime = Field(...)
    order_status: str


class Order(OrderIn):
    id: int
