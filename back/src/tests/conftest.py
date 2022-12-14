import pytest
from app.config import settings
from starlette.testclient import TestClient

from app.server import app


@pytest.fixture(scope="module")
def test_app():
    with TestClient(app) as client:   # context manager will invoke startup event 
        yield client

@pytest.fixture
def api_url():
    def api_url_function(url):
        return f"{settings.PROJECT_API_VERSION}/{url}"
    return api_url_function

