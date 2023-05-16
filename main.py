from typing import Union
from fastapi import FastAPI,Depends

import os
from dotenv import load_dotenv
from pathlib import Path
from api.v1 import auth_endpoints,operation_endpoints

from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated


app = FastAPI()

# v1
app.include_router(auth_endpoints.router, prefix="/v1")
app.include_router(operation_endpoints.router, prefix="/v1")


@app.get('/')
def root():
    return {"Hello":"World"}




