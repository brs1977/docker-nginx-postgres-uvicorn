import json
import pytest
from app.config import settings
from app.db.repository import users



def test_create_user(test_app, monkeypatch):
    test_request_payload = {"name": "Пользователь 1"}
    test_response_payload = {"id": 1, "name": "Пользователь 1"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(users, "post", mock_post)

    response = test_app.post(f"{settings.PROJECT_API_VERSION}/users/", content=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_user_invalid_json(test_app):
    response = test_app.post(f"{settings.PROJECT_API_VERSION}/users/", content=json.dumps({"names": "Пользователь 4"}))
    assert response.status_code == 422

def test_read_user(test_app, monkeypatch):
    test_data = {"id": 1, "name": "Пользователь 1"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(users, "get", mock_get)

    response = test_app.get(f"{settings.PROJECT_API_VERSION}/users/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_user_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(users, "get", mock_get)

    response = test_app.get(f"{settings.PROJECT_API_VERSION}/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

    response = test_app.get(f"{settings.PROJECT_API_VERSION}/users/0")
    assert response.status_code == 422


def test_read_all_users(test_app, monkeypatch):
    test_data = [
        {"name": "Пользователь 1", "id": 1},
        {"name": "Пользователь 2", "id": 2},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(users, "get_all", mock_get_all)

    response = test_app.get(f"{settings.PROJECT_API_VERSION}/users/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_user(test_app, monkeypatch):
    test_update_data = {"name": "someone", "id": 1}

    async def mock_get(id):
        return True

    monkeypatch.setattr(users, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(users, "put", mock_put)

    response = test_app.put(f"{settings.PROJECT_API_VERSION}/users/1/", content=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [999, {"name": "foo"}, 404],
        [1, {"name": "1"}, 404],
        [0, {"name": "foo"}, 422],
    ],
)
def test_update_user_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(users, "get", mock_get)

    response = test_app.put(f"{settings.PROJECT_API_VERSION}/users/{id}/", content=json.dumps(payload),)
    assert response.status_code == status_code


def test_remove_user(test_app, monkeypatch):
    test_data = {"name": "Пользователь 1", "id": 1}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(users, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(users, "delete", mock_delete)

    response = test_app.delete(f"{settings.PROJECT_API_VERSION}/users/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_user_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(users, "get", mock_get)

    response = test_app.delete(f"{settings.PROJECT_API_VERSION}/users/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

    response = test_app.delete(f"{settings.PROJECT_API_VERSION}/users/0/")
    assert response.status_code == 422