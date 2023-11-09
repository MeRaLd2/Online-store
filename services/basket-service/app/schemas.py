from pydantic import BaseModel


class Basket(BaseModel):
    id: int
    name: str
    description: str
    price: float

    class Config:
        from_attributes = True

class BasketCreate(BaseModel):
    name: str
    description: str
    price: float

class BasketUpdate(BaseModel):
    name: str
    description: str
    price: float