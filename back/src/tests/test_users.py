import json

import pytest

from app.api import crud


def test_create_user(test_app, monkeypatch):
    test_request_payload = {"name": "Пользователь 1"}
    test_response_payload = {"id": 1, "name": "Пользователь 1"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/users/", content=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


# def test_create_user_invalid_json(test_app):
#     response = test_app.post("/users/", content=json.dumps({"name": "Пользователь 1"}))
#     print(response)
#     print(response.status_code)
#     assert response.status_code == 422

#     response = test_app.post("/users/", content=json.dumps({"name": "1"}))
#     assert response.status_code == 422


def test_read_user(test_app, monkeypatch):
    test_data = {"id": 1, "name": "Пользователь 1"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/users/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_user_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

    response = test_app.get("/users/0")
    assert response.status_code == 422


def test_read_all_users(test_app, monkeypatch):
    test_data = [
        {"name": "Пользователь 1", "id": 1},
        {"name": "Пользователь 2", "id": 2},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/users/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_user(test_app, monkeypatch):
    test_update_data = {"name": "someone", "id": 1}

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/users/1/", content=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == test_update_data


# @pytest.mark.parametrize(
#     "id, payload, status_code",
#     [
#         [1, {}, 422],
#         [999, {"name": "foo"}, 404],
#         [1, {"name": "1"}, 422],
#         [0, {"name": "foo"}, 422],
#     ],
# )
# def test_update_user_invalid(test_app, monkeypatch, id, payload, status_code):
#     async def mock_get(id):
#         return None

#     monkeypatch.setattr(crud, "get", mock_get)

#     response = test_app.put(f"/users/{id}/", data=json.dumps(payload),)
#     assert response.status_code == status_code


def test_remove_user(test_app, monkeypatch):
    test_data = {"name": "Пользователь 1", "id": 1}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/users/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_user_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/users/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

    response = test_app.delete("/users/0/")
    assert response.status_code == 422