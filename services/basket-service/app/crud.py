from .schemas import Basket, BasketUpdate
from sqlalchemy.orm import Session
from .database import models

def get_baskets(db: Session, limit: int = 10, offset: int = 0):
    return db.query(models.Basket) \
        .offset(offset) \
        .limit(limit) \
        .all()

def get_basket(db: Session, basket_id: int):
    return db.query(models.Basket) \
        .filter(models.Basket.id == basket_id) \
        .first()


def create_basket(db: Session, item: Basket):

    db_item = models.Basket(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return item


def update_basket(db: Session, basket_id: int, basket_update: BasketUpdate):
    result = db.query(models.Basket) \
        .filter(models.Basket.id == basket_id) \
        .update(basket_update.dict())
    db.commit()

    if result == 1:
        return get_basket(db, basket_id)
    return None

def delete_basket(db: Session, basket_id: int):
    result = db.query(models.Basket) \
        .filter(models.Basket.id == basket_id) \
        .delete()
    db.commit()
    return result == 1