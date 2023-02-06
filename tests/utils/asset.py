from fastapi.testclient import TestClient

from config.config import settings


def create_asset(client: TestClient, headers: str) -> dict:  # type: ignore

    asset_data = {"title": "Asset Title", "asset_type": "image"}
    asset_files = {"file": ("asset.png", open("./tests/asset.png", "rb").read())}
    response = client.post(
        f"{settings.API_V1_STR}/asset/", data=asset_data, headers=headers, files=asset_files  # type: ignore
    )
    if response.status_code == 200:
        response = response.json()
        return response  # type: ignore
    return None  # type: ignore
