from pydantic import BaseModel,Field, EmailStr
from typing import Union
from utils.custom_types import PyObjectId
from bson import ObjectId

class Operation(BaseModel):
    id:PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    first_operand: int
    second_operand: int
    total=int


class OperationInput(BaseModel):
    a: int
    b: int

class OperationCreating(BaseModel):
    first_operand: int
    second_operand: int
    total:int




class OperationViewModel(BaseModel):
    id:PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    first_operand: Union[int, None] = None
    second_operand: Union[int, None] = None
    total: Union[int, None] = None
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "first_operand":2,
                "second_operand":3,
                "total": 5,
                "id":"643e78087beae247272083d2",
            }
        }



class TotalViewModel(BaseModel):
    total: Union[int, None] = None
