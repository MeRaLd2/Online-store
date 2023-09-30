from typing import List
from fastapi import FastAPI, Depends, HTTPException
from app import schemas
from . import crud

app = FastAPI(title='Сервис продуктов онлайн-магазина')


@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate):
    return crud.create_product(product)

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int):
    product = crud.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return product

@app.get("/products/", response_model=List[schemas.Product])
def read_products(limit: int = 10, offset: int = 0):
    return crud.get_products(limit=limit, offset=offset)

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductUpdate):
    updated_product = crud.update_product(product_id, product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return updated_product

@app.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int):
    deleted_product = crud.delete_product(product_id)
    if deleted_product is None:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return deleted_product