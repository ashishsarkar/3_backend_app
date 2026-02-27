"""Integration tests: locations search API (Elasticsearch mocked)."""
import unittest.mock as mock
import pytest


@pytest.fixture(autouse=True)
def mock_es_search():
    """Mock Elasticsearch so location tests run without a live ES cluster."""
    sample_results = [
        {
            "id": "BOM", "name": "Mumbai", "code": "BOM",
            "type": "city", "country": "India", "state": "Maharashtra",
            "description": "Chhatrapati Shivaji Maharaj International Airport",
            "aliases": "Bombay CSIA", "score": 24.1,
        },
        {
            "id": "IN-MH", "name": "Maharashtra", "code": "MH",
            "type": "state", "country": "India", "state": "Maharashtra",
            "description": "State — Mumbai, Pune, Nagpur",
            "aliases": "Mumbai state", "score": 12.9,
        },
    ]
    with mock.patch(
        "app.elasticsearch_client.search_locations",
        new=mock.AsyncMock(return_value=sample_results),
    ):
        yield sample_results


def test_location_search_returns_results(client):
    r = client.get("/api/locations/search", params={"q": "mum"})
    assert r.status_code == 200
    data = r.json()
    assert "results" in data
    assert data["total"] >= 1


def test_location_search_response_shape(client):
    r = client.get("/api/locations/search", params={"q": "mum"})
    data = r.json()
    assert "query" in data
    assert "total" in data
    assert "results" in data
    assert data["query"] == "mum"


def test_location_result_fields(client):
    r = client.get("/api/locations/search", params={"q": "mum"})
    result = r.json()["results"][0]
    for field in ("id", "name", "code", "type", "country"):
        assert field in result, f"Missing field: {field}"


def test_location_search_missing_query_returns_422(client):
    """q param is required — missing it should return 422."""
    r = client.get("/api/locations/search")
    assert r.status_code == 422


def test_location_search_with_type_filter(client):
    r = client.get("/api/locations/search", params={"q": "mum", "type": "city"})
    assert r.status_code == 200
    # ES mock called — assert we get back the mocked city result
    results = r.json()["results"]
    assert len(results) >= 1


def test_location_search_size_parameter(client):
    r = client.get("/api/locations/search", params={"q": "mum", "size": 3})
    assert r.status_code == 200


def test_location_search_size_too_large_returns_422(client):
    """size > 20 should be rejected."""
    r = client.get("/api/locations/search", params={"q": "mum", "size": 25})
    assert r.status_code == 422


def test_location_search_total_matches_results_length(client):
    r = client.get("/api/locations/search", params={"q": "mum"})
    data = r.json()
    assert data["total"] == len(data["results"])
