"""Integration tests: extended flight search — partial match, city name, missing routes."""


def test_flight_search_by_origin_city_name(client):
    """Search by origin city name 'Kolkata' matches CCU flights."""
    r = client.get("/api/flights/search", params={"origin": "Kolkata"})
    assert r.status_code == 200
    flights = r.json()["flights"]
    assert len(flights) >= 1
    for f in flights:
        assert f["origin"] == "CCU"


def test_flight_search_by_destination_city_name(client):
    """Search by destination city name 'Mumbai' matches BOM destination."""
    r = client.get("/api/flights/search", params={"destination": "Mumbai"})
    assert r.status_code == 200
    flights = r.json()["flights"]
    assert len(flights) >= 1
    for f in flights:
        assert f["destination"] == "BOM"


def test_cok_to_ccu_route_exists(client):
    """Kochi → Kolkata route is in the DB (was previously missing)."""
    r = client.get("/api/flights/search", params={"origin": "COK", "destination": "CCU"})
    assert r.status_code == 200
    flights = r.json()["flights"]
    assert len(flights) == 1
    assert flights[0]["origin"] == "COK"
    assert flights[0]["destination"] == "CCU"


def test_ccu_departures_covers_major_hubs(client):
    """Kolkata must depart to all major hubs."""
    r = client.get("/api/flights/search", params={"origin": "CCU"})
    destinations = {f["destination"] for f in r.json()["flights"]}
    expected = {"DEL", "BOM", "BLR", "COK"}
    assert expected.issubset(destinations), f"Missing CCU routes: {expected - destinations}"


def test_search_no_origin_returns_all(client):
    """Without filters, all flights are returned."""
    r = client.get("/api/flights/search")
    assert len(r.json()["flights"]) >= 40


def test_search_unknown_origin_returns_empty(client):
    r = client.get("/api/flights/search", params={"origin": "ZZZ"})
    assert r.status_code == 200
    assert r.json()["flights"] == []


def test_flight_price_is_positive(client):
    flights = client.get("/api/flights/search").json()["flights"]
    for f in flights:
        assert f["price"] > 0, f"Flight {f['id']} has non-positive price"


def test_flight_response_has_all_fields(client):
    flights = client.get("/api/flights/search").json()["flights"]
    required = {"id", "origin", "destination", "price", "airline", "departureTime", "arrivalTime"}
    for f in flights:
        missing = required - set(f.keys())
        assert not missing, f"Flight {f['id']} missing fields: {missing}"
