"""Integration tests: confirmations API (uses Redis; with default no Redis returns [])."""


def test_confirmations_log_default(client):
    """GET /api/confirmations/log without Redis returns empty list (app handles missing Redis)."""
    r = client.get("/api/confirmations/log")
    assert r.status_code == 200
    data = r.json()
    assert "confirmations" in data
    assert isinstance(data["confirmations"], list)
