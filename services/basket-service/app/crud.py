import asyncio
from .schemas import Basket, Product, Products
from sqlalchemy.orm import Session
from .database import models
import aiohttp
from . import config
from typing import List

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

async def fetch_product_data(product_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{cfg.PRODUCT_SERVICE_ENTRYPOINT}apartments/{product_id}") as response:
            product_data = await response.json()
    return product_data

async def fetch_multiple_product_data(product_ids) -> List[Product]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_single_product_data(session, product_id) for product_id in product_ids]
        product_data_list = await asyncio.gather(*tasks)
    return product_data_list

async def fetch_single_product_data(session, product_id):
    async with session.get(f"{cfg.PRODUCT_SERVICE_ENTRYPOINT}apartments/{product_id}") as response:
        product_data = await response.json()
    return product_data

async def fetch_products_data(products_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{cfg.PRODUCT_SERVICE_ENTRYPOINT}apartments/{products_id}") as response:
            products_data = await response.json()
    return products_data


async def create_basket(db: Session, item: Basket):

    db_item = models.Basket(
        id=item.id,
        mail=item.mail,
        products_id=item.products_id
    )

    products = await fetch_multiple_product_data(item.products_id)
    products = Products(**products)

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