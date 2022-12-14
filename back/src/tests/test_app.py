from starlette.testclient import TestClient

from app.server import app
from app.config import settings

def test_users(test_app, api_url):
    response = test_app.post(api_url("users"))
    assert response.status_code == 422 
