"""Unit tests for booking router (ID generation and error responses)."""
import pytest


def test_booking_generate_id_format():
    """Booking IDs start with BK and are 12 chars total (BK + 10 alphanumeric)."""
    from app.routers.booking import _generate_id
    bid = _generate_id()
    assert bid.startswith("BK")
    assert len(bid) == 12
    assert bid[2:].isalnum()
    assert bid[2:].isupper() or not bid[2:].islower()  # digits or uppercase


def test_get_booking_404(client):
    """GET /api/booking/nonexistent returns 404."""
    r = client.get("/api/booking/nonexistent-id-123")
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()

    
