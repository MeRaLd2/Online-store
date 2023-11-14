from pydantic import BaseModel, EmailStr
from typing import List

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float

    class Config:
        from_attributes = True

class Basket(BaseModel):
    id: int
    products_id: List[int]
    mail: EmailStr

class Notification(BaseModel):
    mail: EmailStr
    products: List[Product]