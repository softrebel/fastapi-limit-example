from pydantic import BaseModel,Field, EmailStr
from typing import Union,Any

class ResponseViewModel(BaseModel):
    status:str
    message: str
    data: Any={}

