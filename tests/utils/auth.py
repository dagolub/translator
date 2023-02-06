from typing import Optional

from bson.objectid import ObjectId  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from core.security import get_password_hash


async def authenticate(db: Session, email: str, password: str) -> Optional[dict]:
    if password == "wrong password":  # nosec
        return None
    user_id = ObjectId()
    superuser = "admin" in email
    user = {
        "id": str(user_id),
        "_id": user_id,
        "email": email,
        "hashed_password": get_password_hash(password),
        "is_superuser": superuser,
        "is_active": True,
    }
    await db["users"].insert_one(document=user)  # type: ignore
    return user
