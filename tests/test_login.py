from typing import Any

import pytest  # type: ignore
from fastapi.testclient import TestClient  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

import crud
from config.config import settings
from core.deps import get_db
from main import app
from tests.utils.db import fake_db
from tests.utils.user import create_user

app.dependency_overrides[get_db] = fake_db


class Storage:
    reset_password_token = None


def send_email_test(**kwargs: Any) -> None:
    if "environment" in kwargs:
        Storage.reset_password_token = kwargs["environment"]["link"].split("token=")[1]

    return None


login_data = {
    "username": settings.FIRST_SUPERUSER,
    "password": settings.FIRST_SUPERUSER_PASSWORD,
}

incorrect_login_data = {
    "username": "FIRST_SUPERUSER",
    "password": "wrong password",
}


def test_login_access_token_if_user_not_authenticated(client: TestClient) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/access-token", data=incorrect_login_data
    )
    tokens = r.json()
    assert r.status_code == 400  # nosec
    assert "Incorrect email or password" in tokens.values()  # nosec


def _test_login_access_token_if_user_not_active(
    client: TestClient, mocker: Any
) -> None:
    mock_crud_user_is_active = mocker.patch("crud.user.is_active")
    mock_crud_user_is_active.return_value = False
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 400  # nosec
    assert "Inactive user" in tokens.values()  # nosec


def test_recover_password_not_existing_user(client: TestClient) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/password-recovery/not_existing_email@gmail.com"
    )
    tokens = r.json()
    assert r.status_code == 404  # nosec
    assert (  # nosec
        "The user with this username does not exist in the system." in tokens.values()
    )


def test_recover_password(client: TestClient, mocker: Any) -> None:
    mocker.patch("core.utils.send_email", side_effect=send_email_test)
    r = client.post(
        f"{settings.API_V1_STR}/password-recovery/{settings.FIRST_SUPERUSER}"
    )
    result = r.json()
    assert r.status_code == 200  # nosec
    assert result["msg"] == "Password recovery email sent"  # nosec


def test_reset_password_invalid_token(client: TestClient) -> None:
    form_data = {
        "new_password": "mysupersecret__new__password",
        "token": "encoded_password_reset_jwt_token",
    }
    r = client.post(
        f"{settings.API_V1_STR}/reset-password/",
        json=form_data,
    )
    assert r.status_code == 400  # nosec
    assert "Invalid token" in r.json().values()  # nosec


@pytest.mark.asyncio
async def test_reset_password_inactive_user(
    client: TestClient, superuser_token_headers: str, db: Session, mocker: Any
) -> None:
    user, user_id = create_user(client, superuser_token_headers)
    mocker.patch("core.utils.send_email", side_effect=send_email_test)
    user["id"] = user_id  # type: ignore
    r = client.post(f"{settings.API_V1_STR}/password-recovery/{user['username']}")  # type: ignore
    await crud.user.update(db, db_obj=user, obj_in={"is_active": False})  # type: ignore
    form_data = {
        "new_password": "mysupersecret__new__password",
        "token": Storage.reset_password_token,
    }
    r = client.post(
        f"{settings.API_V1_STR}/reset-password/",
        json=form_data,
    )
    assert r.status_code == 400  # nosec
    assert "Inactive user" in r.json().values()  # nosec


def test_reset_password(
    client: TestClient, mocker: Any, superuser_token_headers: str
) -> None:
    user, user_id = create_user(client, superuser_token_headers)
    mocker.patch("core.utils.send_email", side_effect=send_email_test)
    user["id"] = user_id  # type: ignore
    r = client.post(f"{settings.API_V1_STR}/password-recovery/{user['username']}")  # type: ignore
    form_data = {
        "new_password": "mysupersecret__new__password",
        "token": Storage.reset_password_token,
    }
    r = client.post(
        f"{settings.API_V1_STR}/reset-password/",
        json=form_data,
    )
    assert r.status_code == 200  # nosec
    assert {"msg": "Password updated successfully"} == r.json()  # nosec


@pytest.mark.asyncio
async def test_reset_password_not_exist_user(
    client: TestClient, mocker: Any, superuser_token_headers: str, db: Session
) -> None:
    user, user_id = create_user(client, superuser_token_headers)
    mocker.patch("core.utils.send_email", side_effect=send_email_test)
    user["id"] = user_id  # type: ignore
    r = client.post(f"{settings.API_V1_STR}/password-recovery/{user['username']}")  # type: ignore
    form_data = {
        "new_password": "mysupersecret__new__password",
        "token": Storage.reset_password_token,
    }
    await crud.user.remove(db=db, object_id=user_id)  # type: ignore  # nosec
    r = client.post(
        f"{settings.API_V1_STR}/reset-password/",
        json=form_data,
    )
    assert r.status_code == 404  # nosec
    assert {  # nosec
        "detail": "The user with this username does not exist in the system."
    } == r.json()
