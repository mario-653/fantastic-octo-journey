import pytest
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_index_returns_200(client):
    """GET / should return HTTP 200 OK."""
    response = client.get("/")
    assert response.status_code == 200


def test_index_content_type_is_html(client):
    """GET / response Content-Type should be text/html."""
    response = client.get("/")
    assert "text/html" in response.content_type


def test_index_body_contains_hello_world(client):
    """GET / response body should contain the string 'Hello, World!'."""
    response = client.get("/")
    assert b"Hello, World!" in response.data