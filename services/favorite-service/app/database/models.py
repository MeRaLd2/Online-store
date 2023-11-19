from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship
from .database import Base


class FavoriteItem(Base):
    __tablename__ = 'favorite_items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    product_id = Column(Integer)

    #product = relationship("Product", back_populates="favorite_item")