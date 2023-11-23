from starlette.responses import JSONResponse
from .schemas import FeedbackUpdate, FeedbackCreate, Feedback
from .database import models
from typing import List


def get_feedbacks(skip: int = 0, limit: int = 10) -> List[models.Feedback]:
    return models.Feedback.objects \
        .skip(skip) \
        .limit(limit)


def add_feedback(feedback: FeedbackCreate) -> models.Feedback:
    new_feedback = models.Feedback(**feedback.model_dump())
    new_feedback.save()

    return new_feedback


def db_model_to_feedback(feedback: models.Feedback) -> Feedback:
    return Feedback(
        id=feedback.id,
        product_id=feedback.product_id,
        title=feedback.title,
        description=feedback.description
    )


def get_feedback_by_uid(uid: str) -> Feedback:
    feedback = models.Feedback.objects(id=uid).first()

    if feedback is not None:
        return db_model_to_feedback(feedback)


def update_feedback_by_uid(uid: str, feedback_update: FeedbackUpdate) -> Feedback:
    feedback = models.Feedback.objects(id=uid).first()

    if feedback is None:
        return None

    feedback.title = feedback_update.title
    feedback.description = feedback_update.description

    feedback.save()
    return db_model_to_feedback(feedback)


def remove_feedback_by_uid(uid: str):
    feedback = models.Feedback.objects(id=uid).first()

    if feedback is None:
        return JSONResponse(status_code=404, content={"message": "feedback not found"})

    feedback.delete()
    return JSONResponse(status_code=200, content={"message": "Deleted"})
