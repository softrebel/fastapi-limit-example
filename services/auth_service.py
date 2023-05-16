from models import User
from configs import db
from fastapi.encoders import jsonable_encoder

class AuthService:
    def __init__(self):
        pass

    async def get_user(self,username: str) -> User:
        user = await db["user"].find_one({"username": username})
        if user:
            return User(**user)

