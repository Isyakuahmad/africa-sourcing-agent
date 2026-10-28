from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint_reports_service_status():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["app"] == "Africa Sourcing Agent"


def test_api_info_endpoint():
    with TestClient(app) as client:
        response = client.get("/api")

    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "Africa Sourcing Agent"
    assert payload["version"]
    assert payload["docs"] == "/docs"


def test_openapi_document_is_available():
    with TestClient(app) as client:
        response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "Africa Sourcing Agent"
