from .schemas import Delivery
from sqlalchemy.orm import Session
from .database import models
from sqlalchemy import func
from geoalchemy2 import Geometry

def get_deliveries(db: Session, limit: int = 1, offset: int = 0):
    return db.query(models.Delivery) \
        .offset(offset) \
        .limit(limit) \
        .all()

def get_delivery(db: Session, delivery_id: int):
    return db.query(models.Delivery) \
        .filter(models.Delivery.id == delivery_id) \
        .first()

def get_nearby_deliveries(db: Session, latitude: float, longitude: float, radius: float):
    location = func.ST_GeogFromText(f'POINT({latitude} {longitude})', type_=Geometry)
    deliveries = db.query(models.Delivery).filter(
        func.ST_DWithin(models.Delivery.location, location, radius)
    ).all()
    return deliveries

def add_delivery(db: Session, delivery: Delivery):
    db_item = models.Delivery(
        id=delivery.id,
        address=delivery.address,
        rooms=delivery.rooms,
        area=delivery.area,
        latitude=delivery.latitude,
        longitude=delivery.longitude,
        location=f'POINT({delivery.latitude} {delivery.longitude})'
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return delivery

def update_delivery(db: Session, delivery_id: int, updated_delivery: Delivery):
    db_delivery = db.query(models.Delivery).filter(models.Delivery.id == delivery_id).first()

    if db_delivery:
        db_delivery.recipient_name = updated_delivery.recipient_name
        db_delivery.address = updated_delivery.address
        db_delivery.delivery_time = updated_delivery.delivery_time
        db_delivery.package_weight = updated_delivery.package_weight
        db_delivery.latitude = updated_delivery.latitude
        db_delivery.longitude = updated_delivery.longitude
        db_delivery.location = f'POINT({updated_delivery.latitude} {updated_delivery.longitude})'

        db.commit()
        return db_delivery

    return None

def delete_delivery(db: Session, delivery_id: int):
    result = db.query(models.Delivery) \
        .filter(models.Delivery.id == delivery_id) \
        .delete()
    db.commit()
    return result == 1