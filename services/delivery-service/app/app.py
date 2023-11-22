from fastapi import FastAPI, Depends, Query
from starlette.responses import JSONResponse
from .schemas import Delivery, DeliveryQuery
from sqlalchemy.orm import Session
from . import crud, config
import typing
import logging
from .database import DB_INITIALIZER


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=2,
    format="%(levelname)-9s %(message)s"
)


cfg: config.Config = config.load_config()

logger.info(
    'Конфигурация сервиса загружена:\n' +
    f'{cfg.json()}'
)


logger.info('Инициализация базы данных...')
SessionLocal = DB_INITIALIZER.init_database(str(cfg.POSTGRES_DSN))

app = FastAPI(
    title='Delivery service'
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get(
    "/deliveries/{delivery_id}", status_code=201, response_model=Delivery,
    summary='Получить доставку по ID',
    tags = ['deliveries']
)
async def get_delivery(
        delivery_id: int,
        db: Session = Depends(get_db)
    ) -> Delivery:
    item = crud.get_delivery(db, delivery_id)
    if item is not None:
        return item
    return JSONResponse(status_code=404, content={"message": "Доставка не найдена"})

@app.post(
    "/deliveries",
    status_code=201,
    response_model=Delivery,
    summary='Добавить доставку в базу',
    tags = ['deliveries']
)
async def add_delivery(
        delivery: Delivery,
        db: Session = Depends(get_db)
    ) -> Delivery:
    item = crud.add_delivery(db, delivery)
    if item is not None:
        return item
    return JSONResponse(status_code=404, content={"message": f"Доставка с ID {delivery.id} уже существует в базе."})

@app.delete(
    "/deliveries/{delivery_id}",
    summary='Удалить доставку по ID',
    tags = ['deliveries']
)
async def delete_delivery(
        delivery_id: int,
        db: Session = Depends(get_db)
    ):
    deleted = crud.delete_delivery(db, delivery_id)
    if deleted:
        return JSONResponse(status_code=204, content={"message": "Доставка успешно удалена"})
    return JSONResponse(status_code=404, content={"message": "Доставка не найдена"})

@app.put(
    "/deliveries/{delivery_id}",
    status_code=201,
    response_model=Delivery,
    summary='Обновить информацию о доставке',
    tags = ['deliveries']
)
async def update_delivery(
        delivery_id: int,
        updated_delivery: Delivery,
        db: Session = Depends(get_db)
    ) -> Delivery:
    item = crud.update_delivery(db, delivery_id, updated_delivery)
    if item is not None:
        return item
    return JSONResponse(status_code=404, content={"message": "Доставка не найдена"})


@app.get(
    "/deliveries",
    summary='Возвращает список точек доставок',
    response_model=list[Delivery],
    tags = ['deliveries']
)
async def get_deliveries(
        city_name: str = Query(None, description="Город"),
        limit: int = Query(10, description="Макс. количество записей"),
        offset: int = Query(0, description="Смещение записей"),
        radius: float = Query(None, description="Радиус"),
        latitude: float = Query(None, description="Широта"),
        longitude: float = Query(None, description="Долгота"),
        db: Session = Depends(get_db)
    ) -> typing.List[Delivery]:

    delivery_query = DeliveryQuery(
        limit=limit,
        offset=offset,
        city_name=city_name,
        radius=radius*1000,
        latitude=latitude,
        longitude=longitude
    )

    delivery = crud.get_deliveries(db, delivery_query)

    return delivery
