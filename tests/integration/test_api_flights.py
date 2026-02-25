"""Integration tests: flights API (DB + cache path)."""


def test_root_returns_service_info(client):
    """GET / returns service name and docs link."""
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data["service"] == "3_backend_app"
    assert data["docs"] == "/docs"
    assert "databases" in data
    assert "redis" in data["databases"]


def test_flights_search_returns_seeded_flights(client):
    """GET /api/flights/search returns flights from seeded DB (no cache)."""
    r = client.get("/api/flights/search")
    assert r.status_code == 200
    data = r.json()
    assert "flights" in data
    assert len(data["flights"]) >= 1
    flight = data["flights"][0]
    assert "id" in flight
    assert "origin" in flight
    assert "destination" in flight
    assert "price" in flight


def test_flights_search_with_origin_destination(client):
    """GET /api/flights/search?origin=DEL&destination=BOM returns matching flights."""
    r = client.get("/api/flights/search", params={"origin": "DEL", "destination": "BOM"})
    assert r.status_code == 200
    data = r.json()
    assert "flights" in data
    for f in data["flights"]:
        assert f["origin"] == "DEL"
        assert f["destination"] == "BOM"


def test_flights_get_by_id(client):
    """GET /api/flights/:id returns flight detail."""
    r = client.get("/api/flights/search")
    assert r.status_code == 200
    flights = r.json()["flights"]
    assert len(flights) > 0
    fid = flights[0]["id"]
    r2 = client.get(f"/api/flights/{fid}")
    assert r2.status_code == 200
    assert r2.json()["id"] == fid


def test_flights_get_404(client):
    """GET /api/flights/nonexistent returns 404."""
    r = client.get("/api/flights/nonexistent-id")
    assert r.status_code == 404
