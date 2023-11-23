from .schemas import Product, ProductUpdate
from sqlalchemy.orm import Session
from .database import models

def get_products(db: Session, limit: int = 10, offset: int = 0):
    return db.query(models.Product) \
        .offset(offset) \
        .limit(limit) \
        .all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product) \
        .filter(models.Product.id == product_id) \
        .first()


def create_product(db: Session, item: Product):

    db_item = models.Product(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return item


def update_product(db: Session, product_id: int, product_update: ProductUpdate):
    result = db.query(models.Product) \
        .filter(models.Product.id == product_id) \
        .update(product_update.dict())
    db.commit()

    if result == 1:
        return get_product(db, product_id)
    return None

def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return product
    return None