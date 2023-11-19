from pydantic import BaseModel

class FavoriteItem(BaseModel):
    id: int
    name: str
    description: str
    product_id: int

    class Config:
        from_attributes = True