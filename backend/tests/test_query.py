from fastapi.testclient import TestClient
from app.main import app


def test_query_happy_path():

    with TestClient(app) as client:

        response = client.post(
            "/query",
            json={
                "question": "Who is Harry Potter?"
            }
        )

        assert response.status_code == 200
        assert "answer" in response.json()
        assert "sources" in response.json()


def test_query_invalid_input():

    with TestClient(app) as client:

        response = client.post(
            "/query",
            json={}
        )

        assert response.status_code == 422