from fastapi.testclient import TestClient
import pytest

from api.main import app
from api.config import settings


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_root_endpoint(client: TestClient) -> None:
    """Test the root endpoint returns correct documentation links."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs_url" in data
    assert "redoc_url" in data


def test_good_dates_endpoint(client: TestClient) -> None:
    """Test the good dates endpoint with valid input."""
    response = client.post(
        "/good-dates/",
        json={
            "birth_date": "1990-01-01",
            "match_on_single_digit": True,
            "year": 2024,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "dates" in data
    assert "numerology_number" in data
    assert "number_meaning" in data
    assert "total_matches" in data
    assert isinstance(data["dates"], list)
    assert all(isinstance(d, str) for d in data["dates"])


def test_good_dates_invalid_input(client: TestClient) -> None:
    """Test the good dates endpoint with invalid input."""
    response = client.post(
        "/good-dates/",
        json={
            "birth_date": "invalid-date",
            "match_on_single_digit": True,
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data


def test_cache_clear_unauthorized(client: TestClient) -> None:
    """Test cache clear endpoint requires API key."""
    response = client.post("/cache/clear")
    assert response.status_code == 403


def test_cache_clear_authorized(client: TestClient) -> None:
    """Test cache clear endpoint with valid API key."""
    response = client.post(
        "/cache/clear",
        headers={"X-API-Key": settings.admin_api_key},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Cache cleared successfully"


def test_request_id_header(client: TestClient) -> None:
    """Test that responses include request ID header."""
    response = client.get("/")
    assert "X-Request-ID" in response.headers
    assert len(response.headers["X-Request-ID"]) > 0


def test_rate_limiting(client: TestClient) -> None:
    """Test rate limiting kicks in after too many requests."""
    # Make many requests quickly
    for _ in range(70):  # More than our 60/minute limit
        client.get("/")

    # Next request should be rate limited
    response = client.get("/")
    assert response.status_code == 429
    assert "Retry-After" in response.headers
