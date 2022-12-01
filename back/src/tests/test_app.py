from starlette.testclient import TestClient

from app.server import app

client = TestClient(app)


def test_ping():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == [{"datname":"postgres"},{"datname":"db_dev"},{"datname":"template1"},{"datname":"template0"}]