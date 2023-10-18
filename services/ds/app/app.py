from fastapi import FastAPI, Depends, Query
from starlette.responses import JSONResponse
from .schemas import Delivery
from sqlalchemy.orm import Session
from . import crud, config, geo_functions
import typing
import logging
from .database import DB_INITIALIZER

# Настройка логгирования
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=2,
    format="%(levelname)-9s %(message)s"
)

# Загрузка конфигурации
cfg: config.Config = config.load_config()

logger.info(
    'Конфигурация сервиса загружена:\n' +
    f'{cfg.json()}'
)

# Инициализация базы данных
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
    summary='Получить доставку по ID'
)
async def get_delivery(
        delivery_id: int,
        db: Session = Depends(get_db)
    ) -> Delivery:
    item = crud.get_delivery(db, delivery_id)
    if item is not None:
        return item
    return JSONResponse(status_code=404, content={"message": "Доставка не найдена"})

@app.get(
    "/deliveries",
    summary='Возвращает список доставок',
    response_model=list[Delivery]
)
async def get_deliveries(
        limit: int = 1,
        offset: int = 0,
        db: Session = Depends(get_db)
    ) -> typing.List[Delivery]:
    return crud.get_deliveries(db, limit=limit, offset=offset)

@app.post(
    "/deliveries",
    status_code=201,
    response_model=Delivery,
    summary='Добавить доставку в базу'
)
async def add_delivery(
        delivery: Delivery,
        db: Session = Depends(get_db)
    ) -> Delivery:
    item = crud.add_delivery(db, delivery)
    if item is not None:
        return item
    return JSONResponse(status_code=404, content={"message": f"Доставка с ID {delivery.id} уже существует в базе."})
