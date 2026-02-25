"""Unit tests for confirmations router (with mocked Redis)."""
import unittest.mock as mock
import pytest


def test_confirmations_log_returns_list_from_redis(client):
    """GET /api/confirmations/log returns { confirmations: [...] } from Redis."""
    with mock.patch("app.routers.confirmations.confirmations_log_recent", return_value=[
        {"booking_id": "BK1", "status": "confirmed", "type": "flight", "created_at": "2025-02-20T10:00:00Z"},
    ]) as m:
        r = client.get("/api/confirmations/log")
    assert r.status_code == 200
    data = r.json()
    assert "confirmations" in data
    assert len(data["confirmations"]) == 1
    assert data["confirmations"][0]["booking_id"] == "BK1"
    m.assert_called_once_with(limit=10)


def test_confirmations_log_respects_limit(client):
    """GET /api/confirmations/log?limit=3 passes limit to Redis (capped at 50)."""
    with mock.patch("app.routers.confirmations.confirmations_log_recent", return_value=[]) as m:
        client.get("/api/confirmations/log", params={"limit": 3})
    m.assert_called_once_with(limit=3)


def test_confirmations_log_caps_limit_at_50(client):
    """GET /api/confirmations/log?limit=100 is capped at 50 by the router."""
    with mock.patch("app.routers.confirmations.confirmations_log_recent", return_value=[]) as m:
        client.get("/api/confirmations/log", params={"limit": 100})
    m.assert_called_once_with(limit=50)
