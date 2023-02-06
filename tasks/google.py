from copy import copy

import crud
import schemas
from service.trans import Translator  # type: ignore


async def translate(translator: schemas.Translator, db):
    db_obj = copy(translator)  # type: ignore
    translator["text_translated"] = Translator().translate(translator["text"])  # type: ignore
    translator["status"] = schemas.TranslateStatus.FINISHED  # type: ignore
    await crud.translator.update(db, db_obj=db_obj, obj_in=translator)
    print("Background task")
