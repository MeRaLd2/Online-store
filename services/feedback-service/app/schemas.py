from pydantic import BaseModel, BaseConfig, Field, validator
from uuid import UUID



class FeedbackBase(BaseModel):
    product_id: int
    title: str
    description: str

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackUpdate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: UUID