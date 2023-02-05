from typing import Any, Optional
from unittest.mock import MagicMock
from bson.objectid import ObjectId  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from fastapi.encoders import jsonable_encoder
from config.config import settings

first_user_id = ObjectId()


class AsyncIterator:
    def __init__(self, seq):
        self.iter = iter(seq)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration


class MongoDbTest(MagicMock):
    users = {}  # type: ignore

    def __init__(self, *args: Any, **kw: Any):

        super().__init__(*args, **kw)
        user = {
            "id": str(first_user_id),
            "_id": first_user_id,
            "email": settings.FIRST_SUPERUSER,
            "hashed_password": "$2b$12$mLRl07VnztvwkE36I0kC1uLiwalJ39mew.A2PKc1g0MRkf1AtdGD6",  # noqa
            "is_superuser": True,
            "is_active": True,
        }
        self.users.setdefault(str(first_user_id), user)

    async def find_one(self, find: dict) -> Optional[dict]:
        if "email" in find:
            for user in self.users:
                if self.users[user].get("email") == find.get("email"):
                    return self.users[user]
                else:
                    pass
        if "_id" in find:
            for user in self.users:
                if user == str(find["_id"]):
                    return self.users[user]

        return None

    def find(self, find):
        if "owner_id" in find:
            for obj in self.users:
                if "owner_id" in self.users[obj]:
                    if self.users[obj].get("owner_id") == find.get("owner_id"):
                        data = type("Asset", (), self.users[obj])
                        setattr(data, "limit", self.limit)
                        setattr(data, "skip", self.skip)
                        delattr(data, "_id")
                        self.finded_object = data
                        return data
        return self

    def skip(self, skip):
        if self.finded_object:
            return self.finded_object
        return self

    def limit(self, limit):
        if self.finded_object:
            return AsyncIterator([self.finded_object])
        return self

    async def insert_one(self, document: dict) -> Optional[type]:
        user_id = ObjectId() if "_id" not in document else document["_id"]
        if type(document) != dict:
            document = jsonable_encoder(document)

        document["id"] = str(user_id)
        document["_id"] = user_id

        # exists = False
        # for u in self.users:
        #     if document["email"] == self.users[u]["email"]:
        #         exists = True
        #
        # user = None
        # if not exists:
        user = self.users.setdefault(document["id"], document)
        user_obj = type("User", (), user)
        setattr(user_obj, "inserted_id", user_id)
        setattr(user_obj, "_id", user_id)
        return user_obj

    async def update_one(self, find: dict, update: dict) -> Optional[dict]:
        current_user = None
        if "email" in find:
            for user in self.users:
                if self.users[user]["email"] == find["email"]:
                    current_user = user
        if "_id" in find:
            for user in self.users:
                if user == str(find["_id"]):
                    current_user = user

        if current_user in self.users:
            for field in update["$set"]:
                self.users[current_user][field] = update["$set"][field]
            return self.users[current_user]
        return None

    async def delete_one(self, find: dict) -> None:
        current_user = None
        if "email" in find:
            for user in self.users:
                if self.users[user]["email"] == find["email"]:
                    current_user = user
        if "_id" in find:
            for user in self.users:
                if user == str(find["_id"]):
                    current_user = user
        if current_user in self.users:
            del self.users[current_user]


db = None


def fake_db() -> Session:
    global db
    if not db:
        db = MongoDbTest()
    return db
