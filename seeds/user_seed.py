from prepare_seed import *
from models.user import UserInput
from configs.authentication import get_password_hash
from configs.database import db
import asyncio
from pymongo import UpdateOne



async def run_seed():
    users = [
        UserInput(fullname="Root",
                  username="admin",
                  disabled=False,
                  hashed_password=get_password_hash('admin')
                  ).dict(),
        UserInput(fullname="Softrebel",
                  username="softrebel",
                  disabled=False,
                  hashed_password=get_password_hash('123456')
                  ).dict(),
    ]

    bulk_operator = [
        UpdateOne(
            {'pk': item['username']},
            {'$setOnInsert': item},
            upsert=True
        ) for item in users
    ]
    await db.user.bulk_write(bulk_operator)

asyncio.run(run_seed())
