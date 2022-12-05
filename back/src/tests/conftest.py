import pytest
from starlette.testclient import TestClient

from app.server import app


@pytest.fixture(scope="module")
def test_app():
    with TestClient(app) as client:   # context manager will invoke startup event 
        yield client
