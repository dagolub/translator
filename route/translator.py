from typing import Any
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session  # type: ignore
import crud
import models
import schemas
from core import deps

router = APIRouter()


@router.post("/", response_model=schemas.Translator)
async def create_translator(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),  # noqa
    translator_in: schemas.TranslatorCreate,
) -> Any:

    translator = await crud.translator.create(
        db, obj_in=jsonable_encoder(translator_in)
    )  # noqa

    return translator


@router.get("/{translator_id}", response_model=schemas.Translator)
async def read_translator_by_id(
    translator_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),  # type: ignore
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    return await crud.translator.get(db, object_id=translator_id)  # type: ignore
