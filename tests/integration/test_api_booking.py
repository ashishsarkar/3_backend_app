"""Integration tests: booking API — create, get, cancel (full flow with DB)."""


def test_create_booking_returns_id_and_status(client):
    """POST /api/booking creates a booking and returns id, status."""
    payload = {
        "type": "flight",
        "flight": {"id": "f1", "airline": "Test", "origin": "DEL", "destination": "BOM", "price": 3500},
        "total": 3500,
        "cardNumber": "4242424242424242",
        "expiry": "12/28",
        "cvv": "123",
    }
    r = client.post("/api/booking", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["id"].startswith("BK")
    assert data["status"] == "confirmed"
    assert data["type"] == "flight"


def test_get_booking_after_create(client):
    """GET /api/booking/:id returns the created booking."""
    payload = {
        "type": "hotel",
        "hotel": {"id": "h1", "name": "Test Hotel", "location": "Mumbai", "price": 5000},
        "total": 5000,
        "cardNumber": "4242424242424242",
        "expiry": "12/28",
        "cvv": "123",
    }
    create_r = client.post("/api/booking", json=payload)
    assert create_r.status_code == 200
    bid = create_r.json()["id"]
    get_r = client.get(f"/api/booking/{bid}")
    assert get_r.status_code == 200
    assert get_r.json()["id"] == bid
    assert get_r.json()["type"] == "hotel"


def test_patch_booking_cancel(client):
    """PATCH /api/booking/:id with status cancelled updates the booking."""
    create_r = client.post("/api/booking", json={
        "type": "flight",
        "flight": {"id": "f1", "price": 1000},
        "total": 1000,
        "cardNumber": "4242",
        "expiry": "12/28",
        "cvv": "123",
    })
    assert create_r.status_code == 200
    bid = create_r.json()["id"]
    patch_r = client.patch(f"/api/booking/{bid}", json={"status": "cancelled"})
    assert patch_r.status_code == 200
    assert patch_r.json()["status"] == "cancelled"
    assert patch_r.json().get("refundStatus") == "initiated"
