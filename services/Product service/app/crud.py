from .schemas import Product, ProductCreate, ProductUpdate
from typing import List

products_data = []

def get_products(limit: int = 10, offset: int = 0) -> List[Product]:
    return products_data[offset:offset + limit]

def get_product(product_id: int) -> Product:
    for product in products_data:
        if product["id"] == product_id:
            return Product(**product)
    return None

def create_product(product_create: ProductCreate) -> Product:
    product_id = len(products_data) + 1
    product = Product(id=product_id, **product_create.dict())
    products_data.append(product.dict())
    return product

def update_product(product_id: int, product_update: ProductUpdate) -> Product:
    for idx, product in enumerate(products_data):
        if product["id"] == product_id:
            updated_product = Product(id=product_id, **product_update.dict())
            products_data[idx] = updated_product.dict()
            return updated_product
    return None

def delete_product(product_id: int) -> Product:
    for product in products_data:
        if product["id"] == product_id:
            deleted_product = products_data.pop(products_data.index(product))
            return Product(**deleted_product)
    return None