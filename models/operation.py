from pydantic import BaseModel,Field, EmailStr
from typing import Union
from utils.custom_types import PyObjectId

class Operation(BaseModel):
    id:PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    first_operand: int
    second_operand: int
    result=int


class OperationInput(BaseModel):
    a: int
    b: int

class OperationViewModel(BaseModel):
    a: Union[int, None] = None
    b: Union[int, None] = None
    result: Union[int, None] = None
