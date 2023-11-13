from sqlalchemy import Column, ForeignKey, Integer, String, Float, ARRAY
from .database import Base

class Basket(Base):
    __tablename__ = 'baskets'

    id = Column(Integer, primary_key=True, index=True)
    mail = Column(String)
    products_id = Column(ARRAY(Integer), nullable=False)