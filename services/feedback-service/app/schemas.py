from pydantic import BaseModel, BaseConfig, Field, validator
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue
from typing import Optional, List, Any, Annotated
from bson import ObjectId
from uuid import UUID


class ObjectIdPydanticAnnotation:
    @classmethod
    def validate_object_id(cls, v: Any, handler) -> str:
        if isinstance(v, ObjectId):
            return str(v)
        s = handler(v)
        if ObjectId.is_valid(s):
            return s
        else:
            raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, _handler) -> core_schema.CoreSchema:
        if source_type is not str:
            raise ValueError("source_type должен быть строкой")
        return core_schema.no_info_wrap_validator_function(
            cls.validate_object_id,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError('Недопустимый ObjectId')
        return ObjectId(value)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(format='ObjectId')

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