from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Float
from sqlalchemy.orm import relationship
from .database import Base
from geoalchemy2 import Geometry

class Delivery(Base):
    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    rooms = Column(Integer)
    area = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    location = Column(Geometry("POINT", srid=4326))
