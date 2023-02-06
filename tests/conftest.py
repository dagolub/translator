from typing import Any, Dict, Generator

import pytest  # type: ignore
from fastapi.testclient import TestClient  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from config.config import settings
from db.session import client as AsyncIOMotorClient
from main import app
from tests.utils.auth import authenticate
from tests.utils.db import fake_db

# from core.deps import get_db
# from db.session import database
from tests.utils.user import authentication_token_from_email
from tests.utils.utils import get_superuser_token_headers


@pytest.fixture
def event_loop() -> Any:
    loop = AsyncIOMotorClient.get_io_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def db() -> Generator:
    return fake_db()  # type: ignore


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient, session_mocker: Any) -> Dict[str, str]:
    session_mocker.patch("crud.user.authenticate", side_effect=authenticate)
    loop = AsyncIOMotorClient.get_io_loop()
    return loop.run_until_complete(get_superuser_token_headers(client))


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    loop = AsyncIOMotorClient.get_io_loop()

    return loop.run_until_complete(
        authentication_token_from_email(
            client=client, email=settings.EMAIL_TEST_USER, db=db  # type: ignore
        )
    )
