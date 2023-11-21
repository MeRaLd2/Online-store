from typing import List
from fastapi import FastAPI, Depends, HTTPException
from app import schemas
from . import crud, config
from .database import DB_INITIALIZER
from sqlalchemy.orm import Session

cfg: config.Config = config.load_config()

SessionLocal = DB_INITIALIZER.init_database(str(cfg.POSTGRES_DSN))


app = FastAPI(title='Сервис продуктов онлайн-магазина')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.Product, db: Session = Depends(get_db)):
    existing_product = crud.get_product(db, product.id)  # Замените на соответствующий метод

    if existing_product:
        raise HTTPException(status_code=400, detail="Такой продукт уже существует")
    return crud.create_product(db, product)


@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return product


@app.get("/products/", response_model=List[schemas.Product])
def read_products(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    return crud.get_products(db, limit=limit, offset=offset)

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    updated_product = crud.update_product(db, product_id, product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return updated_product

@app.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted_product = crud.delete_product(db, product_id)
    if deleted_product is None:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return deleted_product