from pydantic import BaseModel
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
    mail: str

class Notification(BaseModel):
    mail: str
    products: List[Product]