from typing import List
from fastapi import FastAPI, Depends, HTTPException
from app import schemas
from . import crud, config
import typing
import logging
from .database import DB_INITIALIZER
from sqlalchemy.orm import Session
from . import broker

cfg: config.Config = config.load_config()

message_producer = broker.MessageProducer(
    dsn=cfg.RABBITMQ_DSN.unicode_string(),
    exchange_name=cfg.EXCHANGE_NAME,
    queue_name=cfg.QUEUE_NAME,
)

SessionLocal = DB_INITIALIZER.init_database(str(cfg.POSTGRES_DSN))


app = FastAPI(title='Сервис корзины онлайн-магазина')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post(
    "/baskets/",
    response_model=schemas.Basket,
    tags = ['baskets']
)
async def create_basket(basket: schemas.Basket, db: Session = Depends(get_db)):
    existing_basket = crud.get_basket(db, basket.id)

    if existing_basket:
        raise HTTPException(status_code=400, detail="Такой набор продуктов уже существует")
    basket = await crud.create_basket(db, basket)
    return basket

@app.get(
    "/uploads/{basket_id}",
    response_model=schemas.Basket,
    tags = ['baskets']
)
async def upload_order(basket_id: int, db: Session = Depends(get_db)):
    uploaded_basket = await crud.upload_order(db, basket_id, message_producer)
    if uploaded_basket is None:
        raise HTTPException(status_code=404, detail="Набор продукт не найден")
    return uploaded_basket

@app.get(
    "/baskets/{basket_id}",
    response_model=schemas.Basket,
    tags = ['baskets']
)
def read_basket(basket_id: int, db: Session = Depends(get_db)):
    basket = crud.get_basket(db, basket_id)
    if basket is None:
        raise HTTPException(status_code=404, detail="Набор продукт не найден")
    return basket


@app.get(
    "/baskets/",
    response_model=List[schemas.Basket],
    tags = ['baskets']
)
def read_baskets(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    return crud.get_baskets(db, limit=limit, offset=offset)

@app.put(
    "/baskets/{basket_id}",
    response_model=schemas.Basket,
    tags = ['baskets']
)
def update_basket(basket_id: int, basket: schemas.Basket, db: Session = Depends(get_db)):
    updated_basket = crud.update_basket(db, basket_id, basket)
    if updated_basket is None:
        raise HTTPException(status_code=404, detail="Набор продукт не найден")
    return updated_basket

@app.delete(
    "/baskets/{basket_id}",
    response_model=schemas.Basket,
    tags = ['baskets']
)
def delete_basket(
    basket_id: int,
    db: Session = Depends(get_db)
):
    deleted_basket = crud.delete_basket(db, basket_id)
    if deleted_basket is None:
        raise HTTPException(status_code=404, detail="Набор продуктов не найден")
    return deleted_basket