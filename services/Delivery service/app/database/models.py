from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Float
from sqlalchemy.orm import relationship
from .database import Base
from geoalchemy2 import Geometry

class Delivery(Base):
    __tablename__ = 'delivery'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    package_weight = Column(Integer)
    longitude = Column(Float)
    latitude = Column(Float)
    location = Column(Geometry("POINT", srid=4326))