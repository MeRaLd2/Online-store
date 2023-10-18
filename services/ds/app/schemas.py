from pydantic import BaseModel

class Delivery(BaseModel):
    id: int
    recipient_name: str
    address: str
    delivery_time: str
    package_weight: float
    latitude: float
    longitude: float

    class Config:
        from_attributes = True