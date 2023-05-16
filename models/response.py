
from typing import Union, Any, Generic, TypeVar
from pydantic import BaseModel, Field, validator, ValidationError
from pydantic.generics import GenericModel
from bson import ObjectId

DataT = TypeVar('DataT')




class Response(GenericModel, Generic[DataT]):
    status: int | None
    message: str | None
    data: DataT | None
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}



    # @validator('error', always=True)
    # def check_consistency(cls, v, values):
    #     if v is not None and values['data'] is not None:
    #         raise ValueError('must not provide both data and error')
    #     if v is None and values.get('data') is None:
    #         raise ValueError('must provide data or error')
    #     return v
