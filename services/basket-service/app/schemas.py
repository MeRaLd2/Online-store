from pydantic import BaseModel
from typing import List

class Products(BaseModel):
    id: int
    name: str
    description: str
    price: float
    amount: int

    class Config:
        from_attributes = True

class ProductsCreate(BaseModel):
    name: str
    description: str
    price: float
    amount: int

class ProductsUpdate(BaseModel):
    name: str
    description: str
    price: float
    amount: int


class Basket(BaseModel):
    id: int
    products: List[Products]
    mail: str