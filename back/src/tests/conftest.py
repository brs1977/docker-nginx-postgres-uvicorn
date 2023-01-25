import pytest
from tests.db_utils import create_fake_db
from starlette.testclient import TestClient
from app.config import settings
from app.server import app

class CookieConfigurableTestClient(TestClient):
    _access_token = None

    def set_access_token(self, token):
        self._access_token = token

    def reset(self):
        self._access_token = None

    def request(self, *args, **kwargs):
        cookies = kwargs.get("cookies")
        if cookies is None and self._access_token:
            kwargs["headers"] = {"Cookie": f"access-token={self._access_token}"}

        return super().request(*args, **kwargs)

def pytest_sessionstart(session):
    create_fake_db()

@pytest.fixture(scope="module")
def test_app():
    with CookieConfigurableTestClient(app) as client:   # context manager will invoke startup event 
        yield client

@pytest.fixture
def api_url():
    def api_url_function(url):
        return f"{settings.PROJECT_API_VERSION}/{url}"
    return api_url_function
