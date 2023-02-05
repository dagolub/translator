from typing import Any, Dict, Optional, TypeVar, Union  # type: ignore
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from core.security import get_password_hash, verify_password
from crud.base import CRUDBase
from db.base_class import Base
from models.user import User
from schemas.user import UserCreate, UserUpdate

ModelType = TypeVar("ModelType", bound=Base)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    @staticmethod
    async def get_by_email(db: Session, email: str) -> Optional[User]:
        pass
        return await db[User.__tablename__].find_one({"email": email})  # type: ignore

    async def update(  # type: ignore
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        update_data = obj_in

        if "password" in update_data:  # type: ignore
            hashed_password = get_password_hash(update_data["password"])  # type: ignore
            del update_data["password"]  # type: ignore
            update_data["hashed_password"] = hashed_password  # type: ignore
        if "email" in update_data:
            del update_data["email"]  # type: ignore

        return await super().update(db, db_obj, update_data)

    async def authenticate(
        self, db: AsyncIOMotorClient, *, email: str, password: str
    ) -> Optional[User]:
        current_user = await self.get_by_email(db, email=email)
        if not current_user:
            return None
        if not verify_password(password, current_user["hashed_password"]):  # type: ignore
            return None
        return current_user

    @staticmethod
    def is_active(current_user: User) -> bool:
        return current_user["is_active"]  # type: ignore

    @staticmethod
    def is_superuser(current_user: User) -> bool:
        return current_user["is_superuser"]  # type: ignore


user = CRUDUser(User)
