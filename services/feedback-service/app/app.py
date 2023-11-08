from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse

import logging
from typing import List, Annotated
from uuid import UUID

from . import config, crud
from .database import MongoDB
from .schemas import FeedbackUpdate, FeedbackCreate, Feedback


################
## INITIALIZE ##
################
logger = logging.getLogger("feedback-service")
logging.basicConfig(level=logging.INFO, 
                    format="[%(levelname)s][%(name)s][%(filename)s, line %(lineno)d]: %(message)s")

logger.info("Service configuration loading...")
cfg: config.Config = config.load_config()

logger.info(
    'Service configuration loaded:\n' +
    f'{cfg.model_dump_json(by_alias=True, indent=4)}'
)

logger.info("Service database loading...")
MongoDB(mongo_dsn=str(cfg.mongo_dsn))
logger.info("Service database loaded")



app = FastAPI(
    version='0.0.1',
    title='feedback service'
)


@app.get("/feedbacks", 
         summary="Returns all feedbacks",
         response_model=List[Feedback],
         tags=['feedbacks']
)
async def get_feedbacks(skip: int = 0, limit: int = 10):
    return crud.get_feedbacks(skip, limit)


@app.post("/feedbacks", 
         summary="Add new feedback",
         response_model=Feedback,
         tags=['feedbacks']
)
async def add_feedback(feedback: FeedbackCreate) -> Feedback:
    return crud.add_feedback(feedback)


@app.get("/feedbacks/{feedback_id}", 
         summary="Get feedback by id",
         tags=['feedbacks']
)
async def get_feedback_uid(feedback_id: str) -> Feedback:
    feedback = crud.get_feedback_by_uid(feedback_id)
    if feedback is None:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    return feedback


@app.put("/feedbacks/{feedback_id}", 
         summary="Update feedback info by id",
         tags=['feedbacks']
)
async def update_feedback(feedback_id: str, feedback_update: FeedbackUpdate) -> Feedback:
    feedback = crud.update_feedback_by_uid(feedback_id, feedback_update)
    if feedback is None:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    return feedback


@app.delete("/feedbacks/{feedback_id}", 
         summary="Delete feedback by id",
         tags=['feedbacks']
)
async def delete_feedback(feedback_id: str) -> Feedback:
    return crud.remove_feedback_by_uid(feedback_id)

