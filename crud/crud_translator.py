from typing import TypeVar  # type: ignore
from crud.base import CRUDBase
from db.base_class import Base
from models.translator import Translator
from schemas.translator import TranslatorCreate, TranslatorUpdate

ModelType = TypeVar("ModelType", bound=Base)


class CRUDUser(CRUDBase[Translator, TranslatorCreate, TranslatorUpdate]):
    pass


translator = CRUDUser(Translator)
