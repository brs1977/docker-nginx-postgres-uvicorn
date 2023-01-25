import pytest
from app.schemas.users import UserSchema
from app.api import security 

from app.db.repository import users

user_data = UserSchema(
    role_id=4,
    email="user@example.com",
    username="adm",
    password=security.hash_password("adm"),
    fio="string",
    is_active=True
)


def login(request_data, test_app, api_url, monkeypatch):
    async def mock_get_by_username(username):
        return user_data
    monkeypatch.setattr(users, 'get_by_username', mock_get_by_username)
    
    response = test_app.post(api_url("auth/login"), data=request_data)    
    return response

def test_login(test_app, api_url, monkeypatch):
    request_data = {"username": "adm", "password": "adm"}
    response = login(request_data, test_app, api_url, monkeypatch)
    assert response.status_code == 201
    assert "access-token" in response.cookies
    assert response.cookies["access-token"]

def test_login_with_invalid_password(test_app, api_url, monkeypatch):
    request_data = {"username": "adm", "password": "ad"}
    response = login(request_data, test_app, api_url, monkeypatch)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_user_detail_forbidden_without_token(test_app, api_url):
    response = test_app.get(api_url("auth/me"))
    assert response.status_code == 401

def test_login_me(test_app, api_url, monkeypatch):
    request_data = {"username": "adm", "password": "adm"}
    response = login(request_data, test_app, api_url, monkeypatch)

    assert response.status_code == 201
    token = response.cookies['access-token']

    response = test_app.get(
        api_url("auth/me"),
        headers = {"Cookie": f"access-token={token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "adm"

@pytest.mark.freeze_time("2023-01-25")
def test_user_detail_forbidden_with_expired_token(test_app, api_url, freezer, monkeypatch):
    request_data = {"username": "adm", "password": "adm"}
    response = login(request_data, test_app, api_url, monkeypatch)
        
    freezer.move_to("'2023-01-26'")
    token = response.cookies['access-token']

    test_app.set_access_token(token)
    response = test_app.get(
        api_url("auth/me"),
        # headers = {"Cookie": f"access-token={token}"}
    )
    assert response.status_code == 401
