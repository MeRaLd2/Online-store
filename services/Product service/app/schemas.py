from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float

class ProductUpdate(BaseModel):
    name: str
    description: str
    price: float