from pydantic import BaseModel
from typing import Optional

class Delivery(BaseModel):
    id: int
    address: str
    package_weight: float
    latitude: float
    longitude: float

    class Config:
        from_attributes = True


class DeliveryQuery(BaseModel):
    city_name: Optional[str]
    limit: int = 1
    offset: int = 0
    latitude: Optional[float]
    longitude: Optional[float]
    radius: Optional[float]

    class Config:
        from_attributes = True