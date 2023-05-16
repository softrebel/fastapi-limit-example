from typing import Union
from fastapi import FastAPI,Depends,Request

import os
from dotenv import load_dotenv
from pathlib import Path
from api.v1 import auth_endpoints,operation_endpoints

from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated
from fastapi.exceptions import HTTPException
from utils.handle_exceptions import exception_handlers


app = FastAPI(exception_handlers=exception_handlers)
# app=FastAPI()
# v1
app.include_router(auth_endpoints.router, prefix="/v1")
app.include_router(operation_endpoints.router, prefix="/v1")



@app.get('/')
def root(request:Request):
    clientIp = request.client.host
    return {"Hello":"World","ip":clientIp}




