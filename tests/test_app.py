import json
import pytest
from app import app


@pytest.fixture
def client():
    """Create and configure a Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_route_success(client):
    """Test that the index route returns HTTP 200 and loads HTML template."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.content_type.startswith("text/html")
    html_content = response.data.decode("utf-8")
    assert "CI/CD" in html_content
    assert "Production CI/CD Pipeline" in html_content
    assert "Commit to Production" in html_content


def test_health_endpoint_structure(client):
    """Test that the /health endpoint returns HTTP 200 with JSON payload."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.content_type == "application/json"

    data = json.loads(response.data)
    assert data.get("status") == "healthy"
    assert "version" in data
    assert "hostname" in data
    assert len(data["hostname"]) > 0


def test_health_endpoint_values(client):
    """Test that /health returns a valid version string."""
    response = client.get("/health")
    data = json.loads(response.data)
    # APP_VERSION should be a non-empty string format e.g. 1.0.0 or semantic version
    assert isinstance(data["version"], str)
    assert len(data["version"]) > 0


def test_404_not_found(client):
    """Test that requesting an invalid route returns standard HTTP 404."""
    response = client.get("/invalid-nonexistent-endpoint")
    assert response.status_code == 404


def test_api_info_endpoint(client):
    """Test that /api/info returns HTTP 200 with JSON metadata payload."""
    response = client.get("/api/info")
    assert response.status_code == 200
    assert response.content_type == "application/json"
    data = json.loads(response.data)
    assert data.get("service") == "cicd-assignment-backend"
    assert "version" in data
    assert "hostname" in data
    assert data.get("cluster") == "docker-swarm"
