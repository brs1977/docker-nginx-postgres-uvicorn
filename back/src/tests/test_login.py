import pytest
import asyncio
# from app.schemas.users import UserCreate
# from app.utils.users import create_user, create_user_token


# def test_login(test_app):
#     request_data = {"username": "vader@deathstar.com", "password": "rainbow"}
    
#     response = test_app.post("/auth", data=request_data)
#     assert response.status_code == 200
#     assert response.json()["token_type"] == "bearer"
#     assert response.json()["expires"] is not None
#     assert response.json()["access_token"] is not None


# def test_login_with_invalid_password(test_app):
#     request_data = {"username": "vader@deathstar.com", "password": "unicorn"}
#     response = test_app.post("/auth", data=request_data)
#     assert response.status_code == 400
#     assert response.json()["detail"] == "Incorrect email or password"


# def test_user_detail(test_app):
#     # Create user token to see user info
#     loop = asyncio.get_event_loop()
#     token = loop.run_until_complete(create_user_token(user_id=1))
#     response = test_app.get(
#         "/users/me",
#         headers={"Authorization": f"Bearer {token['token']}"}
#     )
#     assert response.status_code == 200
#     assert response.json()["id"] == 1
#     assert response.json()["email"] == "vader@deathstar.com"
#     assert response.json()["name"] == "Darth"


# def test_user_detail_forbidden_without_token(test_app):
#     response = test_app.get("/users/me")
#     assert response.status_code == 401


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