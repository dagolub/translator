from typing import Generic, Type, TypeVar, Optional, List, Union, Dict, Any
from sqlalchemy.orm import Session  # type: ignore
from pydantic import BaseModel
from bson.objectid import ObjectId
from db.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: Session, object_id: str) -> Optional[ModelType]:
        entity = await db[self.model.__tablename__].find_one({"_id": ObjectId(object_id)})  # type: ignore
        if entity:
            entity["id"] = str(entity["_id"])
            return entity
        else:
            return None

    async def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        entities = []
        async for entity in db[self.model.__tablename__].find().skip(skip).limit(limit):  # type: ignore
            entity["id"] = str(entity["_id"])  # noqa
            entities.append(entity)
        return entities

    async def get_multi_by_owner_id(
        self, db: Session, owner_id: str, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        entities = []
        async for entity in db[self.model.__tablename__].find(
            {"owner_id": owner_id}
        ).skip(skip).limit(
            limit
        ):  # type: ignore
            if type(entity) is dict:
                entity["id"] = str(entity["_id"])  # noqa

            entities.append(entity)
        return entities

    async def create(self, db: Session, obj_in: dict) -> Optional[ModelType]:  # type: ignore
        entity = await db[self.model.__tablename__].insert_one(document=obj_in)  # type: ignore
        if entity:
            return await self.find_one(db, self.model.__tablename__, entity.inserted_id)  # type: ignore

    async def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        update_data = obj_in
        await db[self.model.__tablename__].update_one(
            {"_id": ObjectId(db_obj["id"])}, {"$set": update_data}  # type: ignore
        )  # type: ignore
        return await self.find_one(db, self.model.__tablename__, ObjectId(db_obj["id"]))  # type: ignore

    async def remove(self, db: Session, object_id: str) -> None:
        await db[self.model.__tablename__].delete_one({"_id": ObjectId(object_id)})

    @staticmethod
    async def find_one(db, table, object_id):
        entity = await db[table].find_one({"_id": ObjectId(object_id)})
        if entity:
            entity["id"] = str(object_id)
            entity["inserted_id"] = str(object_id)
            return entity
        return None
