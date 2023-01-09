import json
import pytest

from app.db.repository import users


def test_create_user(test_app, api_url, monkeypatch):
    test_request_payload = {'role_id': 4, 'username': 'username', 'password': 'password', 'email': 'email@email.com', 'fio': 'fio' }
    test_response_payload = {'id': 1, 'role_id': 4, 'username': 'username', 'password': 'password', 'email': 'email@email.com', 'fio': 'fio' }

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(users, 'post', mock_post)

    response = test_app.post(api_url('users/'), content=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


# def test_create_user_invalid_json(test_app, api_url):
#     response = test_app.post(api_url('users/'), content=json.dumps({'usernames': 'Пользователь 4'}))
#     assert response.status_code == 422

# def test_read_user(test_app, api_url, monkeypatch):
#     test_data = {'id': 1, 'username': 'Пользователь 1'}

#     async def mock_get(id):
#         return test_data

#     monkeypatch.setattr(users, 'get', mock_get)

#     response = test_app.get(api_url('users/1'))
#     assert response.status_code == 200
#     assert response.json() == test_data


# def test_read_user_incorrect_id(test_app, api_url, monkeypatch):
#     async def mock_get(id):
#         return None

#     monkeypatch.setattr(users, 'get', mock_get)

#     response = test_app.get(api_url('users/999'))
#     assert response.status_code == 404
#     assert response.json()['detail'] == 'User not found'

#     response = test_app.get(api_url('users/0'))
#     assert response.status_code == 422


# def test_read_all_users(test_app, api_url, monkeypatch):
#     test_data = [
#         {'username': 'Пользователь 1', 'id': 1},
#         {'username': 'Пользователь 2', 'id': 2},
#     ]

#     async def mock_get_all():
#         return test_data

#     monkeypatch.setattr(users, 'get_all', mock_get_all)

#     response = test_app.get(api_url('users/'))
#     assert response.status_code == 200
#     assert response.json() == test_data


# def test_update_user(test_app, api_url, monkeypatch):
#     test_update_data = {'username': 'someone', 'id': 1}

#     async def mock_get(id):
#         return True

#     monkeypatch.setattr(users, 'get', mock_get)

#     async def mock_put(id, payload):
#         return 1

#     monkeypatch.setattr(users, 'put', mock_put)

#     response = test_app.put(api_url('users/1/'), content=json.dumps(test_update_data))
#     assert response.status_code == 200
#     assert response.json() == test_update_data


# @pytest.mark.parametrize(
#     'id, payload, status_code',
#     [
#         [1, {}, 422],
#         [999, {"username": "foo"}, 404],
#         [0, {"username": "foo"}, 422],
#     ]
# )
# def test_update_user_invalid(test_app, api_url, monkeypatch, id, payload, status_code):
#     async def mock_get(id):
#         return None

#     monkeypatch.setattr(users, 'get', mock_get)

#     response = test_app.put(api_url(f'users/{id}/'), content=json.dumps(payload),)
#     assert response.status_code == status_code


# def test_remove_user(test_app, api_url, monkeypatch):
#     test_data = {'username': 'Пользователь 1', 'id': 1}

#     async def mock_get(id):
#         return test_data

#     monkeypatch.setattr(users, 'get', mock_get)

#     async def mock_delete(id):
#         return id

#     monkeypatch.setattr(users, 'delete', mock_delete)

#     response = test_app.delete(api_url('users/1/'))
#     assert response.status_code == 200
#     assert response.json() == test_data


# def test_remove_user_incorrect_id(test_app, api_url, monkeypatch):
#     async def mock_get(id):
#         return None

#     monkeypatch.setattr(users, 'get', mock_get)

#     response = test_app.delete(api_url('users/999/'))
#     assert response.status_code == 404
#     assert response.json()['detail'] == 'User not found'

#     response = test_app.delete(api_url('users/0/'))
#     assert response.status_code == 422