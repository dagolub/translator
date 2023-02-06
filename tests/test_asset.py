from typing import Dict

import pytest  # type: ignore
from fastapi.testclient import TestClient

from config.config import settings
from core.deps import get_db
from main import app
from tests.utils.asset import create_asset
from tests.utils.db import fake_db

app.dependency_overrides[get_db] = fake_db


@pytest.mark.asyncio
async def test_get_assets(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    create_asset(client, superuser_token_headers)  # type: ignore
    assets = client.get(
        f"{settings.API_V1_STR}/asset/", headers=superuser_token_headers
    ).json()
    assert len(assets) == 1
    # deleted_asset = client.delete(f"{settings.API_V1_STR}/asset/{asset['id']}", headers=superuser_token_headers)
    # assets = client.get(f"{settings.API_V1_STR}/asset/", headers=superuser_token_headers).json()
    # assert len(assets) == 0
