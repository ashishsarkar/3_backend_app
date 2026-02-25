"""Unit tests for health router."""
def test_health_live(client):
    """GET /health/live returns 200 and status ok."""
    r = client.get("/health/live")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_health_ready(client):
    """GET /health/ready returns 200 and checks postgres and mongo (mongo mocked in conftest)."""
    r = client.get("/health/ready")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] in ("ok", "degraded")
    assert "postgres" in data
    assert "mongodb" in data
