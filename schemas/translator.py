from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TranslateStatus(str, Enum):
    FINISHED = "finished"
    PENDING = "pending"


class TranslatorBase(BaseModel):
    text: Optional[str] = None
    text_translated: Optional[str] = None
    status: Optional[TranslateStatus]


class TranslatorCreate(TranslatorBase):
    pass


class TranslatorUpdate(TranslatorBase):
    pass


class TranslatorInDBBase(TranslatorBase):
    id: str
    _id: str

    class Config:
        orm_mode = True


class Translator(TranslatorInDBBase):
    pass


class TranslatorInDB(TranslatorInDBBase):
    hashed_password: str
