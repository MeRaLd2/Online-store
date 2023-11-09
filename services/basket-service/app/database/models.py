from sqlalchemy import Column, ForeignKey, Integer, String, Float
from .database import Base

class Basket(Base):
    __tablename__ = 'baskets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)

