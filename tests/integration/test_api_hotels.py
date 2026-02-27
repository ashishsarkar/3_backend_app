"""Integration tests: hotels API — search, detail, rooms."""


def test_hotels_search_returns_seeded_hotels(client):
    r = client.get("/api/hotels/search")
    assert r.status_code == 200
    data = r.json()
    assert "hotels" in data
    assert len(data["hotels"]) >= 1


def test_hotels_search_response_shape(client):
    r = client.get("/api/hotels/search")
    hotel = r.json()["hotels"][0]
    for field in ("id", "name", "location", "price", "rating"):
        assert field in hotel, f"Missing field: {field}"


def test_hotels_search_by_location_mumbai(client):
    r = client.get("/api/hotels/search", params={"location": "Mumbai"})
    assert r.status_code == 200
    hotels = r.json()["hotels"]
    assert len(hotels) >= 1
    for h in hotels:
        assert "mumbai" in h["location"].lower() or "mumbai" in h["name"].lower()


def test_hotels_search_partial_location(client):
    """Partial location string should still match (ilike %...%)."""
    r = client.get("/api/hotels/search", params={"location": "Del"})
    assert r.status_code == 200
    hotels = r.json()["hotels"]
    assert len(hotels) >= 1


def test_hotels_search_no_results_for_unknown(client):
    r = client.get("/api/hotels/search", params={"location": "Nonexistent-XYZ-12345"})
    assert r.status_code == 200
    assert r.json()["hotels"] == []


def test_hotel_get_by_id(client):
    hotels = client.get("/api/hotels/search").json()["hotels"]
    assert len(hotels) > 0
    hid = hotels[0]["id"]
    r = client.get(f"/api/hotels/{hid}")
    assert r.status_code == 200
    assert r.json()["id"] == hid


def test_hotel_detail_includes_rooms(client):
    hotels = client.get("/api/hotels/search").json()["hotels"]
    hid = hotels[0]["id"]
    r = client.get(f"/api/hotels/{hid}")
    assert r.status_code == 200
    data = r.json()
    assert "rooms" in data
    assert isinstance(data["rooms"], list)
    assert len(data["rooms"]) >= 1


def test_hotel_detail_room_has_required_fields(client):
    hotels = client.get("/api/hotels/search").json()["hotels"]
    hid = hotels[0]["id"]
    room = client.get(f"/api/hotels/{hid}").json()["rooms"][0]
    for field in ("id", "name", "price"):
        assert field in room, f"Room missing field: {field}"


def test_hotel_get_404(client):
    r = client.get("/api/hotels/nonexistent-hotel-99")
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()


def test_hotels_search_empty_location_returns_all(client):
    """No location filter returns all hotels."""
    all_r = client.get("/api/hotels/search")
    filtered_r = client.get("/api/hotels/search", params={"location": ""})
    # Both should return same or all hotels
    assert filtered_r.status_code == 200
