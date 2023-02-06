from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session  # type: ignore

import crud
import models
import schemas
from core import deps
from schemas.translator import TranslateStatus
from tasks.google import translate

router = APIRouter()


@router.post("/", response_model=schemas.Translator)
async def create_translator(
    translator_in: schemas.TranslatorCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    translator_in.status = TranslateStatus.PENDING
    translator = await crud.translator.create(
        db, obj_in=jsonable_encoder(translator_in)  # type: ignore
    )  # noqa
    background_tasks.add_task(translate, translator, db)
    return translator


@router.get("/{translator_id}", response_model=schemas.Translator)
async def read_translator_by_id(
    translator_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),  # type: ignore
    db: Session = Depends(deps.get_db),
) -> Any:
    return await crud.translator.get(db, object_id=translator_id)  # type: ignore
