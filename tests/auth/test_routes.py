import pytest
from async_asgi_testclient import TestClient
from fastapi import status


async def test_register(client: TestClient) -> None:
    json_data = {
        "email": "email@fake.com",
        "password": "123456!S",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "fake_username"
        }

    resp = await client.post(
        "/auth/register",
        json=json_data,
    )

    resp_json = resp.json()

    assert resp.status_code == status.HTTP_201_CREATED
    resp_json.pop("id", None)
    json_data.pop("password", None)
    assert resp_json == json_data


async def test_register_email_taken(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    json_data = {
        "email": "email@fake.com",
        "password": "123456!S",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "fake_username"
    }

    resp = await client.post(
        "/auth/register",
        json=json_data,
    )

    resp_json = resp.json()

    assert resp.status_code == status.HTTP_400_BAD_REQUEST