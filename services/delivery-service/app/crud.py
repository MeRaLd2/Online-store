from .schemas import Delivery, DeliveryQuery
from sqlalchemy.orm import Session
from .database import models
from sqlalchemy import func
from geoalchemy2 import Geometry
from .geo_functions import geocode_city

def get_deliveries(db: Session, limit: int = 1, offset: int = 0):
    return db.query(models.Delivery) \
        .offset(offset) \
        .limit(limit) \
        .all()

def get_delivery(db: Session, delivery_id: int):
    return db.query(models.Delivery) \
        .filter(models.Delivery.id == delivery_id) \
        .first()

def add_delivery(db: Session, delivery: Delivery):
    db_item = models.Delivery(
        id=delivery.id,
        address=delivery.address,
        package_weight=delivery.package_weight,
        longitude=delivery.longitude,
        latitude=delivery.latitude,
        location=f'POINT({delivery.latitude} {delivery.longitude})'
    )

    if get_delivery(db=db, delivery_id=delivery.id):
        return None

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return delivery

def update_delivery(db: Session, delivery_id: int, updated_delivery: Delivery):
    db_delivery = db.query(models.Delivery).filter(models.Delivery.id == delivery_id).first()

    if db_delivery:
        db_delivery.address = updated_delivery.address
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


def get_deliveries(db: Session, delivery_query: DeliveryQuery):

    query = db.query(models.Delivery)

    if delivery_query.city_name is not None and delivery_query.radius is not None:
        city_coords = geocode_city(delivery_query.city_name)
        if city_coords is not None:
            latitude = city_coords["lat"]
            longitude = city_coords["lng"]
            location = func.ST_GeogFromText(f'POINT({latitude} {longitude})', type_=Geometry)
            query = query.filter(func.ST_DWithin(models.Delivery.location, location, delivery_query.radius))
            query = query.order_by(func.ST_Distance(models.Delivery.location, location))


    if delivery_query.city_name is None and delivery_query.latitude is not None and delivery_query.longitude \
            is not None and delivery_query.radius is not None:
        location = func.ST_GeogFromText(f'POINT({delivery_query.latitude} {delivery_query.longitude})', type_=Geometry)
        query = query.filter(func.ST_DWithin(models.Delivery.location, location, delivery_query.radius))
        query = query.order_by(func.ST_Distance(models.Delivery.location, location))


    query = query.offset(delivery_query.offset).limit(delivery_query.limit)
    delivery = query.all()

    return delivery