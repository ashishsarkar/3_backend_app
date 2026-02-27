"""Unit tests for the seed dataset — validates data integrity without DB."""
from app.db.seed import FLIGHTS_DATA, HOTELS_DATA, PROMOS_DATA


class TestFlightsSeedData:
    def test_minimum_flight_count(self):
        assert len(FLIGHTS_DATA) >= 40, "Should have at least 40 seeded flights"

    def test_all_flights_have_required_fields(self):
        required = {"id", "origin", "origin_city", "destination", "destination_city",
                    "departure_time", "arrival_time", "price", "airline", "duration"}
        for f in FLIGHTS_DATA:
            missing = required - set(f.keys())
            assert not missing, f"Flight {f.get('id')} missing fields: {missing}"

    def test_flight_ids_unique(self):
        ids = [f["id"] for f in FLIGHTS_DATA]
        assert len(ids) == len(set(ids)), "Duplicate flight IDs found"

    def test_flight_prices_positive(self):
        for f in FLIGHTS_DATA:
            assert f["price"] > 0, f"Flight {f['id']} has non-positive price"

    def test_flight_origins_are_iata_codes(self):
        for f in FLIGHTS_DATA:
            assert len(f["origin"]) == 3, f"Origin {f['origin']} should be 3-letter IATA"
            assert f["origin"].isupper(), f"IATA code {f['origin']} should be uppercase"

    def test_ccu_departures_exist(self):
        ccu_flights = [f for f in FLIGHTS_DATA if f["origin"] == "CCU"]
        assert len(ccu_flights) >= 6, "Should have at least 6 CCU departures"

    def test_cok_to_ccu_exists(self):
        """Kochi → Kolkata must be in seed data (was previously missing)."""
        match = [f for f in FLIGHTS_DATA if f["origin"] == "COK" and f["destination"] == "CCU"]
        assert len(match) == 1, "COK→CCU route missing from seed"

    def test_departure_dates_are_2026(self):
        for f in FLIGHTS_DATA:
            assert f["departure_time"].startswith("2026"), \
                f"Flight {f['id']} has old departure date: {f['departure_time']}"


class TestHotelsSeedData:
    def test_minimum_hotel_count(self):
        assert len(HOTELS_DATA) >= 5

    def test_all_hotels_have_required_fields(self):
        required = {"id", "name", "location", "price", "rating"}
        for h in HOTELS_DATA:
            missing = required - set(h.keys())
            assert not missing, f"Hotel {h.get('id')} missing fields: {missing}"

    def test_hotels_have_rooms(self):
        for h in HOTELS_DATA:
            assert "rooms" in h and len(h["rooms"]) >= 1, \
                f"Hotel {h['id']} has no rooms"

    def test_hotel_ratings_in_range(self):
        for h in HOTELS_DATA:
            assert 1 <= h["rating"] <= 5, f"Hotel {h['id']} rating out of range"


class TestPromosSeedData:
    def test_promos_exist(self):
        assert len(PROMOS_DATA) >= 3

    def test_save10_exists(self):
        codes = {p["code"] for p in PROMOS_DATA}
        assert "SAVE10" in codes

    def test_flat500_exists(self):
        codes = {p["code"] for p in PROMOS_DATA}
        assert "FLAT500" in codes

    def test_promo_discount_types_valid(self):
        for p in PROMOS_DATA:
            assert p["discount_type"] in ("percent", "fixed"), \
                f"Promo {p['code']} has invalid discount_type"
