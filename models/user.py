from sqlalchemy import Boolean, Column, String  # type: ignore

from db.base_class import Base


class User(Base):
    __tablename__: str = "translator_users"  # type: ignore
    _id = Column(String, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
