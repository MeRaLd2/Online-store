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


def get_deliveriesgeo(db: Session, deliveries_query: DeliveryQuery):
    class DeliverySpecification:
        def __init__(self):
            self.filters = []
            self.sorting = []

        def by_location(self, latitude, longitude, radius):
            if latitude is not None and longitude is not None and radius is not None:
                location = func.ST_GeogFromText(f'POINT({latitude} {longitude})', type_=Geometry)
                self.filters.append(func.ST_DWithin(models.Delivery.location, location, radius))
                self.sorting.append(func.ST_Distance(models.Delivery.location, location))
            return self

        def by_city(self, city_name, radius):
            if city_name:
                city_coords = geocode_city(city_name)
                if city_coords is not None:
                    latitude = city_coords["lat"]
                    longitude = city_coords["lng"]
                    location = func.ST_GeogFromText(f'POINT({latitude} {longitude})', type_=Geometry)
                    self.filters.append(func.ST_DWithin(models.Delivery.location, location, radius))
                    self.sorting.append(func.ST_Distance(models.Delivery.location, location))
            return self

        def build_filters(self):
            return self.filters

        def build_sorting(self):
            return self.sorting

    query = db.query(models.Delivery)

    if deliveries_query.city_name is not None and deliveries_query.radius is not None:
        delivery_spec = DeliverySpecification().by_city(deliveries_query.city_name, deliveries_query.radius)
        query = query.filter(*delivery_spec.build_filters()).order_by(*delivery_spec.build_sorting())

    if deliveries_query.city_name is None and deliveries_query.latitude is not None and deliveries_query.longitude \
            is not None and deliveries_query.radius is not None:
        delivery_spec = DeliverySpecification().by_location(deliveries_query.latitude, deliveries_query.longitude, deliveries_query.radius)
        query = query.filter(*delivery_spec.build_filters()).order_by(*delivery_spec.build_sorting())

    query = query.offset(deliveries_query.offset).limit(deliveries_query.limit)
    delivery = query.all()

    return delivery