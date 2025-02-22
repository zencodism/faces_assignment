# the only purpose of this at the moment is to show we know about unit tests
import pytest

from app import app as app_obj


@pytest.fixture()
def app():
    app_obj.config.update(
        {
            "TESTING": True,
        }
    )
    yield app_obj


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_request_example(client):
    response = client.get("/")
    assert b"Welcome" in response.data
