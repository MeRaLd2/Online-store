import asyncio
from .schemas import Basket, Product, Notification
from sqlalchemy.orm import Session
from .database import models
import aiohttp
from . import config
from typing import List
from .broker import MessageProducer

cfg: config.Config = config.load_config()

def get_baskets(db: Session, limit: int = 10, offset: int = 0):
    return db.query(models.Basket) \
        .offset(offset) \
        .limit(limit) \
        .all()

def get_basket(db: Session, basket_id: int):
    return db.query(models.Basket) \
        .filter(models.Basket.id == basket_id) \
        .first()

async def fetch_multiple_product_data(product_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_single_product_data(session, product_id) for product_id in product_ids]
        product_data_list = await asyncio.gather(*tasks)

    products = [Product(**data) for data in product_data_list]
    return products

async def fetch_single_product_data(session, product_id):
    async with session.get(f"{cfg.PRODUCT_ENTRYPOINT}products/{product_id}") as response:
        product_data = await response.json()
    return product_data

async def create_basket(db: Session, item: Basket):

    db_item = models.Basket(
        id=item.id,
        mail=item.mail,
        products_id=item.products_id
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return item


def update_basket(db: Session, basket_id: int, basket_update: Basket):
    result = db.query(models.Basket) \
        .filter(models.Basket.id == basket_id) \
        .update(basket_update.dict())
    db.commit()

    if result == 1:
        return get_basket(db, basket_id)
    return None

def delete_basket(db: Session, basket_id: int):
    deleted_basket = db.query(models.Basket).filter(models.Basket.id == basket_id).first()
    if deleted_basket:
        db.delete(deleted_basket)
        db.commit()
        return deleted_basket
    return None

async def upload_order(db: Session, basket_id: int, msg_prod: MessageProducer):
    basket = get_basket(db, basket_id)

    products = await fetch_multiple_product_data(basket.products_id)
    notification = Notification(
        mail=basket.mail,
        products=products
    )

    msg_prod.send_message(notification.json())
    return basket