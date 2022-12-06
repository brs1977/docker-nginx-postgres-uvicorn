from starlette.testclient import TestClient

from app.server import app

client = TestClient(app)


# def test_db():
#     response = client.get("/test")
#     assert response.status_code == 200
#     assert response.json() == [{"datname":"postgres"},{"datname":"db_dev"},{"datname":"template1"},{"datname":"template0"}]

def test_users():
    response = client.post("/api/v1/users")
    assert response.status_code == 422 
