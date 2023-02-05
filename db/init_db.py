from sqlalchemy.orm import Session  # type: ignore
import crud
from config.config import settings
from core.security import get_password_hash
from db import base  # noqa: F401


async def init_db(db: Session) -> None:
    user = await crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = {
            "email": settings.FIRST_SUPERUSER,
            "hashed_password": get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            "is_superuser": True,
            "is_active": True,
            "full_name": "Admin",
        }
        user = await crud.user.create(db, obj_in=user_in)  # noqa: F841
