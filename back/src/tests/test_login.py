import pytest
from app.schemas.users import UserSchema
from app.api import security 

from app.db.repository import users
# import sys
# import json
# import asyncio
# from app.db.repository import users
# from app.server import app
# from app.config import settings
# from httpx import AsyncClient
# from typing import Dict, Generator

# accept: application/json
# Accept-Encoding: gzip, deflate
# Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7
# Connection: keep-alive
# Content-Length: 70
# Content-Type: application/x-www-form-urlencoded
# Cookie: access-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG0iLCJleHAiOjE2NzQ1OTYzNTR9.NdoRGBsrSmcQaEbapcq8LeDO_eTC1IQL0A3IkLzbpkI
# Host: 129.200.0.116:8020
# Origin: http://129.200.0.116:8020
# Referer: http://129.200.0.116:8020/docs
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36

user_data = UserSchema(
    role_id=4,
    email="user@example.com",
    username="adm",
    password=security.hash_password("adm"),
    fio="string",
    is_active=True
)


def test_login(test_app, api_url, monkeypatch):
    async def mock_get_by_username(username):
        return user_data
    monkeypatch.setattr(users, 'get_by_username', mock_get_by_username)

    # async def mock_authenticate_user(username, password):
    #     return user_data
    # monkeypatch.setattr(security, 'authenticate_user', mock_authenticate_user)

    request_data = {"username": "adm", "password": "adm"}
    response = test_app.post(api_url("auth/login"), data=request_data)
    assert response.status_code == 201
    assert "access-token" in response.cookies
    assert response.cookies["access-token"]

def test_login_with_invalid_password(test_app, api_url, monkeypatch):
    async def mock_get_by_username(username):
        return user_data
    monkeypatch.setattr(users, 'get_by_username', mock_get_by_username)

    request_data = {"username": "adm", "password": "ad"}
    response = test_app.post(api_url("auth/login"), data=request_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_user_detail_forbidden_without_token(test_app, api_url):
    response = test_app.get(api_url("auth/me"))
    assert response.status_code == 401

def test_login_me(test_app, api_url, monkeypatch):
    async def mock_get_by_username(username):
        return user_data
    monkeypatch.setattr(users, 'get_by_username', mock_get_by_username)

    request_data = {"username": "adm", "password": "adm"}
    response = test_app.post(api_url("auth/login"), data=request_data)
    assert response.status_code == 201
    token = response.cookies['access-token']

    response = test_app.get(
        api_url("auth/me"),
        headers = {"Cookie": f"access-token={token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "adm"

# @pytest.mark.freeze_time("2015-10-21")
# def test_user_detail_forbidden_with_expired_token(test_app, freezer):
#     user = UserCreate(
#         email="sidious@deathstar.com",
#         name="Palpatine",
#         password="unicorn"
#     )
#     # Create user and use expired token
#     loop = asyncio.get_event_loop()
#     user_db = loop.run_until_complete(create_user(user))
#     freezer.move_to("'2015-11-10'")
#     response = test_app.get(
#         "/users/me",
#         headers={"Authorization": f"Bearer {user_db['token']['token']}"}
#     )
#     assert response.status_code == 401


# from loguru import logger
# from app.utils.users import create_user, create_user_token
# logger.add(sys.stdout)

# @pytest.fixture
# @pytest.mark.anyio
# async def client() -> Generator:
#     async with AsyncClient(app=app, base_url=settings.PROJECT_API_VERSION) as ac:
#         yield ac


# @pytest.mark.anyio
# async def test_get_tokens(client: AsyncClient, api_url, monkeypatch) -> None:
#     user_data = UserSchema(
#         role_id=4,
#         email="user@example.com",
#         username="adm",
#         password=security.hash_password("adm"),
#         fio="string",
#         is_active=True
#     )

#     async def mock_authenticate_user(username, password):
#         return user_data
#     monkeypatch.setattr(security, 'authenticate_user', mock_authenticate_user)

#     request_data = {"username": "adm", "password": "adm"}
#     request = await client.post("auth/login", data=request_data)
#     assert request.status_code == 201

# @pytest.fixture()
# def mock_authenticate_user(monkeypatch):
#     future = asyncio.Future()
#     monkeypatch.patch('security.authenticate_user', return_value=future)
#     return future


