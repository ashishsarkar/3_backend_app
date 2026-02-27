"""Seeds the PostgreSQL database on startup if tables are empty."""

from sqlalchemy.orm import Session
from app.models import Flight, Hotel, Room, Wallet, Promo


FLIGHTS_DATA = [
    # ── Delhi routes ─────────────────────────────────────────────────────────
    {"id": "f1",  "origin": "DEL", "origin_city": "New Delhi",    "destination": "BOM", "destination_city": "Mumbai",            "departure_time": "2026-03-15T06:00:00Z", "arrival_time": "2026-03-15T08:30:00Z", "price": 4500, "airline": "IndiGo",       "duration": "2h 30m"},
    {"id": "f2",  "origin": "DEL", "origin_city": "New Delhi",    "destination": "BLR", "destination_city": "Bengaluru",         "departure_time": "2026-03-15T09:00:00Z", "arrival_time": "2026-03-15T11:30:00Z", "price": 4800, "airline": "Air India",    "duration": "2h 30m"},
    {"id": "f3",  "origin": "DEL", "origin_city": "New Delhi",    "destination": "MAA", "destination_city": "Chennai",           "departure_time": "2026-03-15T07:00:00Z", "arrival_time": "2026-03-15T09:30:00Z", "price": 5100, "airline": "Vistara",     "duration": "2h 30m"},
    {"id": "f4",  "origin": "DEL", "origin_city": "New Delhi",    "destination": "HYD", "destination_city": "Hyderabad",         "departure_time": "2026-03-15T13:00:00Z", "arrival_time": "2026-03-15T15:00:00Z", "price": 4300, "airline": "SpiceJet",    "duration": "2h"},
    {"id": "f5",  "origin": "DEL", "origin_city": "New Delhi",    "destination": "CCU", "destination_city": "Kolkata",           "departure_time": "2026-03-15T05:30:00Z", "arrival_time": "2026-03-15T07:45:00Z", "price": 4100, "airline": "Vistara",     "duration": "2h 15m"},
    {"id": "f6",  "origin": "DEL", "origin_city": "New Delhi",    "destination": "COK", "destination_city": "Kochi",             "departure_time": "2026-03-15T08:30:00Z", "arrival_time": "2026-03-15T11:00:00Z", "price": 5500, "airline": "Air India",    "duration": "2h 30m"},
    {"id": "f7",  "origin": "DEL", "origin_city": "New Delhi",    "destination": "TRV", "destination_city": "Thiruvananthapuram","departure_time": "2026-03-15T14:00:00Z", "arrival_time": "2026-03-15T16:45:00Z", "price": 5800, "airline": "IndiGo",       "duration": "2h 45m"},
    {"id": "f8",  "origin": "DEL", "origin_city": "New Delhi",    "destination": "GOI", "destination_city": "Goa",               "departure_time": "2026-03-15T10:00:00Z", "arrival_time": "2026-03-15T12:15:00Z", "price": 4600, "airline": "Go First",    "duration": "2h 15m"},
    {"id": "f9",  "origin": "DEL", "origin_city": "New Delhi",    "destination": "JAI", "destination_city": "Jaipur",            "departure_time": "2026-03-16T07:00:00Z", "arrival_time": "2026-03-16T08:00:00Z", "price": 2200, "airline": "IndiGo",       "duration": "1h"},
    {"id": "f10", "origin": "DEL", "origin_city": "New Delhi",    "destination": "AMD", "destination_city": "Ahmedabad",         "departure_time": "2026-03-16T09:30:00Z", "arrival_time": "2026-03-16T11:00:00Z", "price": 3100, "airline": "SpiceJet",    "duration": "1h 30m"},
    # ── Mumbai routes ────────────────────────────────────────────────────────
    {"id": "f11", "origin": "BOM", "origin_city": "Mumbai",       "destination": "DEL", "destination_city": "New Delhi",         "departure_time": "2026-03-16T14:00:00Z", "arrival_time": "2026-03-16T16:30:00Z", "price": 5200, "airline": "Air India",    "duration": "2h 30m"},
    {"id": "f12", "origin": "BOM", "origin_city": "Mumbai",       "destination": "BLR", "destination_city": "Bengaluru",         "departure_time": "2026-03-16T06:00:00Z", "arrival_time": "2026-03-16T07:30:00Z", "price": 3800, "airline": "IndiGo",       "duration": "1h 30m"},
    {"id": "f13", "origin": "BOM", "origin_city": "Mumbai",       "destination": "GOI", "destination_city": "Goa",               "departure_time": "2026-03-16T08:00:00Z", "arrival_time": "2026-03-16T09:15:00Z", "price": 2800, "airline": "Go First",    "duration": "1h 15m"},
    {"id": "f14", "origin": "BOM", "origin_city": "Mumbai",       "destination": "COK", "destination_city": "Kochi",             "departure_time": "2026-03-16T11:00:00Z", "arrival_time": "2026-03-16T13:00:00Z", "price": 4200, "airline": "Vistara",     "duration": "2h"},
    {"id": "f15", "origin": "BOM", "origin_city": "Mumbai",       "destination": "HYD", "destination_city": "Hyderabad",         "departure_time": "2026-03-17T07:00:00Z", "arrival_time": "2026-03-17T08:30:00Z", "price": 3500, "airline": "SpiceJet",    "duration": "1h 30m"},
    # ── Bengaluru routes ─────────────────────────────────────────────────────
    {"id": "f16", "origin": "BLR", "origin_city": "Bengaluru",    "destination": "DEL", "destination_city": "New Delhi",         "departure_time": "2026-03-17T05:30:00Z", "arrival_time": "2026-03-17T08:00:00Z", "price": 5000, "airline": "IndiGo",       "duration": "2h 30m"},
    {"id": "f17", "origin": "BLR", "origin_city": "Bengaluru",    "destination": "GOI", "destination_city": "Goa",               "departure_time": "2026-03-17T09:00:00Z", "arrival_time": "2026-03-17T10:00:00Z", "price": 3200, "airline": "Booking Life", "duration": "1h"},
    {"id": "f18", "origin": "BLR", "origin_city": "Bengaluru",    "destination": "MAA", "destination_city": "Chennai",           "departure_time": "2026-03-17T12:00:00Z", "arrival_time": "2026-03-17T13:00:00Z", "price": 2600, "airline": "SpiceJet",    "duration": "1h"},
    {"id": "f19", "origin": "BLR", "origin_city": "Bengaluru",    "destination": "HYD", "destination_city": "Hyderabad",         "departure_time": "2026-03-18T07:00:00Z", "arrival_time": "2026-03-18T08:00:00Z", "price": 2400, "airline": "Air India",    "duration": "1h"},
    {"id": "f20", "origin": "BLR", "origin_city": "Bengaluru",    "destination": "CCU", "destination_city": "Kolkata",           "departure_time": "2026-03-18T15:00:00Z", "arrival_time": "2026-03-18T17:45:00Z", "price": 4700, "airline": "IndiGo",       "duration": "2h 45m"},
    # ── Kolkata routes ───────────────────────────────────────────────────────
    {"id": "f21", "origin": "CCU", "origin_city": "Kolkata",      "destination": "DEL", "destination_city": "New Delhi",         "departure_time": "2026-03-07T06:00:00Z", "arrival_time": "2026-03-07T08:15:00Z", "price": 4100, "airline": "IndiGo",       "duration": "2h 15m"},
    {"id": "f22", "origin": "CCU", "origin_city": "Kolkata",      "destination": "BOM", "destination_city": "Mumbai",            "departure_time": "2026-03-07T09:00:00Z", "arrival_time": "2026-03-07T11:45:00Z", "price": 4900, "airline": "Air India",    "duration": "2h 45m"},
    {"id": "f23", "origin": "CCU", "origin_city": "Kolkata",      "destination": "BLR", "destination_city": "Bengaluru",         "departure_time": "2026-03-07T13:00:00Z", "arrival_time": "2026-03-07T15:30:00Z", "price": 4600, "airline": "SpiceJet",    "duration": "2h 30m"},
    {"id": "f24", "origin": "CCU", "origin_city": "Kolkata",      "destination": "COK", "destination_city": "Kochi",             "departure_time": "2026-03-07T07:30:00Z", "arrival_time": "2026-03-07T10:15:00Z", "price": 5300, "airline": "Vistara",     "duration": "2h 45m"},
    {"id": "f25", "origin": "CCU", "origin_city": "Kolkata",      "destination": "TRV", "destination_city": "Thiruvananthapuram","departure_time": "2026-03-07T11:00:00Z", "arrival_time": "2026-03-07T14:00:00Z", "price": 5600, "airline": "IndiGo",       "duration": "3h"},
    {"id": "f26", "origin": "CCU", "origin_city": "Kolkata",      "destination": "HYD", "destination_city": "Hyderabad",         "departure_time": "2026-03-07T15:00:00Z", "arrival_time": "2026-03-07T17:00:00Z", "price": 4200, "airline": "Air India",    "duration": "2h"},
    {"id": "f27", "origin": "CCU", "origin_city": "Kolkata",      "destination": "GOI", "destination_city": "Goa",               "departure_time": "2026-03-08T06:30:00Z", "arrival_time": "2026-03-08T09:00:00Z", "price": 4800, "airline": "IndiGo",       "duration": "2h 30m"},
    {"id": "f28", "origin": "CCU", "origin_city": "Kolkata",      "destination": "MAA", "destination_city": "Chennai",           "departure_time": "2026-03-08T08:00:00Z", "arrival_time": "2026-03-08T10:30:00Z", "price": 4400, "airline": "SpiceJet",    "duration": "2h 30m"},
    # ── Kerala (Kochi) routes ────────────────────────────────────────────────
    {"id": "f29", "origin": "COK", "origin_city": "Kochi",        "destination": "DEL", "destination_city": "New Delhi",         "departure_time": "2026-03-19T06:00:00Z", "arrival_time": "2026-03-19T08:30:00Z", "price": 5500, "airline": "Air India",    "duration": "2h 30m"},
    {"id": "f30", "origin": "COK", "origin_city": "Kochi",        "destination": "BOM", "destination_city": "Mumbai",            "departure_time": "2026-03-19T08:00:00Z", "arrival_time": "2026-03-19T10:00:00Z", "price": 4200, "airline": "IndiGo",       "duration": "2h"},
    {"id": "f31", "origin": "COK", "origin_city": "Kochi",        "destination": "BLR", "destination_city": "Bengaluru",         "departure_time": "2026-03-19T11:00:00Z", "arrival_time": "2026-03-19T12:15:00Z", "price": 3100, "airline": "SpiceJet",    "duration": "1h 15m"},
    {"id": "f32", "origin": "COK", "origin_city": "Kochi",        "destination": "CCU", "destination_city": "Kolkata",           "departure_time": "2026-03-19T13:00:00Z", "arrival_time": "2026-03-19T15:45:00Z", "price": 5200, "airline": "Vistara",     "duration": "2h 45m"},
    {"id": "f33", "origin": "COK", "origin_city": "Kochi",        "destination": "HYD", "destination_city": "Hyderabad",         "departure_time": "2026-03-19T07:00:00Z", "arrival_time": "2026-03-19T08:30:00Z", "price": 3400, "airline": "IndiGo",       "duration": "1h 30m"},
    {"id": "f34", "origin": "COK", "origin_city": "Kochi",        "destination": "MAA", "destination_city": "Chennai",           "departure_time": "2026-03-19T10:00:00Z", "arrival_time": "2026-03-19T11:15:00Z", "price": 2900, "airline": "SpiceJet",    "duration": "1h 15m"},
    # ── Kerala (Thiruvananthapuram) routes ───────────────────────────────────
    {"id": "f35", "origin": "TRV", "origin_city": "Thiruvananthapuram","destination": "DEL","destination_city": "New Delhi",     "departure_time": "2026-03-20T05:30:00Z", "arrival_time": "2026-03-20T08:15:00Z", "price": 5800, "airline": "Vistara",     "duration": "2h 45m"},
    {"id": "f36", "origin": "TRV", "origin_city": "Thiruvananthapuram","destination": "BOM","destination_city": "Mumbai",        "departure_time": "2026-03-20T09:00:00Z", "arrival_time": "2026-03-20T11:15:00Z", "price": 4700, "airline": "Air India",    "duration": "2h 15m"},
    {"id": "f37", "origin": "TRV", "origin_city": "Thiruvananthapuram","destination": "CCU","destination_city": "Kolkata",       "departure_time": "2026-03-20T11:00:00Z", "arrival_time": "2026-03-20T14:15:00Z", "price": 5900, "airline": "IndiGo",       "duration": "3h 15m"},
    {"id": "f38", "origin": "TRV", "origin_city": "Thiruvananthapuram","destination": "BLR","destination_city": "Bengaluru",     "departure_time": "2026-03-20T14:00:00Z", "arrival_time": "2026-03-20T15:15:00Z", "price": 3300, "airline": "SpiceJet",    "duration": "1h 15m"},
    # ── Chennai & Hyderabad routes ───────────────────────────────────────────
    {"id": "f39", "origin": "MAA", "origin_city": "Chennai",      "destination": "HYD", "destination_city": "Hyderabad",         "departure_time": "2026-03-18T11:30:00Z", "arrival_time": "2026-03-18T12:45:00Z", "price": 2800, "airline": "SpiceJet",    "duration": "1h 15m"},
    {"id": "f40", "origin": "MAA", "origin_city": "Chennai",      "destination": "DEL", "destination_city": "New Delhi",         "departure_time": "2026-03-18T06:00:00Z", "arrival_time": "2026-03-18T08:30:00Z", "price": 5100, "airline": "IndiGo",       "duration": "2h 30m"},
    {"id": "f41", "origin": "MAA", "origin_city": "Chennai",      "destination": "CCU", "destination_city": "Kolkata",           "departure_time": "2026-03-18T13:00:00Z", "arrival_time": "2026-03-18T15:30:00Z", "price": 4800, "airline": "Air India",    "duration": "2h 30m"},
    {"id": "f42", "origin": "MAA", "origin_city": "Chennai",      "destination": "BOM", "destination_city": "Mumbai",            "departure_time": "2026-03-18T09:00:00Z", "arrival_time": "2026-03-18T11:00:00Z", "price": 4000, "airline": "Vistara",     "duration": "2h"},
    {"id": "f43", "origin": "HYD", "origin_city": "Hyderabad",    "destination": "DEL", "destination_city": "New Delhi",         "departure_time": "2026-03-20T07:00:00Z", "arrival_time": "2026-03-20T09:00:00Z", "price": 4300, "airline": "Air India",    "duration": "2h"},
    {"id": "f44", "origin": "HYD", "origin_city": "Hyderabad",    "destination": "BOM", "destination_city": "Mumbai",            "departure_time": "2026-03-20T10:00:00Z", "arrival_time": "2026-03-20T11:30:00Z", "price": 3500, "airline": "IndiGo",       "duration": "1h 30m"},
    {"id": "f45", "origin": "HYD", "origin_city": "Hyderabad",    "destination": "CCU", "destination_city": "Kolkata",           "departure_time": "2026-03-20T14:00:00Z", "arrival_time": "2026-03-20T16:15:00Z", "price": 4500, "airline": "SpiceJet",    "duration": "2h 15m"},
    {"id": "f46", "origin": "HYD", "origin_city": "Hyderabad",    "destination": "BLR", "destination_city": "Bengaluru",         "departure_time": "2026-03-20T08:00:00Z", "arrival_time": "2026-03-20T09:00:00Z", "price": 2600, "airline": "Go First",    "duration": "1h"},
    # ── Goa routes ───────────────────────────────────────────────────────────
    {"id": "f47", "origin": "GOI", "origin_city": "Goa",          "destination": "DEL", "destination_city": "New Delhi",         "departure_time": "2026-03-21T12:00:00Z", "arrival_time": "2026-03-21T14:15:00Z", "price": 4600, "airline": "IndiGo",       "duration": "2h 15m"},
    {"id": "f48", "origin": "GOI", "origin_city": "Goa",          "destination": "BOM", "destination_city": "Mumbai",            "departure_time": "2026-03-21T08:00:00Z", "arrival_time": "2026-03-21T09:15:00Z", "price": 2800, "airline": "SpiceJet",    "duration": "1h 15m"},
    {"id": "f49", "origin": "GOI", "origin_city": "Goa",          "destination": "BLR", "destination_city": "Bengaluru",         "departure_time": "2026-03-21T10:00:00Z", "arrival_time": "2026-03-21T11:00:00Z", "price": 3200, "airline": "Air India",    "duration": "1h"},
    # ── Jaipur, Ahmedabad ────────────────────────────────────────────────────
    {"id": "f50", "origin": "JAI", "origin_city": "Jaipur",       "destination": "BOM", "destination_city": "Mumbai",            "departure_time": "2026-03-22T08:00:00Z", "arrival_time": "2026-03-22T09:45:00Z", "price": 3300, "airline": "SpiceJet",    "duration": "1h 45m"},
    {"id": "f51", "origin": "JAI", "origin_city": "Jaipur",       "destination": "BLR", "destination_city": "Bengaluru",         "departure_time": "2026-03-22T11:00:00Z", "arrival_time": "2026-03-22T13:00:00Z", "price": 4100, "airline": "IndiGo",       "duration": "2h"},
    {"id": "f52", "origin": "AMD", "origin_city": "Ahmedabad",    "destination": "DEL", "destination_city": "New Delhi",         "departure_time": "2026-03-22T10:00:00Z", "arrival_time": "2026-03-22T11:30:00Z", "price": 3100, "airline": "Go First",    "duration": "1h 30m"},
    {"id": "f53", "origin": "AMD", "origin_city": "Ahmedabad",    "destination": "BOM", "destination_city": "Mumbai",            "departure_time": "2026-03-22T07:00:00Z", "arrival_time": "2026-03-22T08:00:00Z", "price": 2200, "airline": "Air India",    "duration": "1h"},
    {"id": "f54", "origin": "AMD", "origin_city": "Ahmedabad",    "destination": "CCU", "destination_city": "Kolkata",           "departure_time": "2026-03-22T13:00:00Z", "arrival_time": "2026-03-22T15:30:00Z", "price": 4600, "airline": "IndiGo",       "duration": "2h 30m"},
]

HOTELS_DATA = [
    {
        "id": "h1",
        "name": "Taj Palace Mumbai",
        "location": "Mumbai",
        "address": "Apollo Bandar, Colaba",
        "lat": 19.076,
        "lng": 72.878,
        "price": 8500,
        "rating": 4.8,
        "image": "/hotel1.jpg",
        "amenities": ["WiFi", "Pool", "Spa"],
        "rooms": [
            {"id": "h1-r1", "name": "Deluxe Room", "price": 8500, "max_guests": 2},
            {"id": "h1-r2", "name": "Suite", "price": 15000, "max_guests": 4},
        ],
    },
    {
        "id": "h2",
        "name": "ITC Maurya Delhi",
        "location": "New Delhi",
        "address": "Diplomatic Enclave",
        "lat": 28.614,
        "lng": 77.209,
        "price": 12000,
        "rating": 4.9,
        "image": "/hotel2.jpg",
        "amenities": ["WiFi", "Pool", "Gym", "Restaurant"],
        "rooms": [
            {"id": "h2-r1", "name": "Executive Room", "price": 12000, "max_guests": 2},
            {"id": "h2-r2", "name": "Presidential Suite", "price": 35000, "max_guests": 6},
        ],
    },
    {
        "id": "h3",
        "name": "Taj West End Bengaluru",
        "location": "Bengaluru",
        "address": "Race Course Road",
        "lat": 12.972,
        "lng": 77.595,
        "price": 9500,
        "rating": 4.7,
        "image": "/hotel3.jpg",
        "amenities": ["WiFi", "Pool", "Spa", "Garden"],
        "rooms": [
            {"id": "h3-r1", "name": "Garden View", "price": 9500, "max_guests": 2},
            {"id": "h3-r2", "name": "Poolside Villa", "price": 22000, "max_guests": 4},
        ],
    },
    {
        "id": "h4",
        "name": "The Oberoi Chennai",
        "location": "Chennai",
        "address": "Egmore",
        "lat": 13.083,
        "lng": 80.271,
        "price": 7800,
        "rating": 4.6,
        "image": "/hotel4.jpg",
        "amenities": ["WiFi", "Pool", "Restaurant"],
        "rooms": [
            {"id": "h4-r1", "name": "Standard Room", "price": 7800, "max_guests": 2},
        ],
    },
    {
        "id": "h5",
        "name": "Park Hyatt Goa",
        "location": "Goa",
        "address": "Cansaulim",
        "lat": 15.299,
        "lng": 74.124,
        "price": 11000,
        "rating": 4.8,
        "image": "/hotel5.jpg",
        "amenities": ["WiFi", "Pool", "Beach", "Spa"],
        "rooms": [
            {"id": "h5-r1", "name": "Beach Villa", "price": 11000, "max_guests": 3},
            {"id": "h5-r2", "name": "Pool Suite", "price": 18000, "max_guests": 4},
        ],
    },
]

PROMOS_DATA = [
    {"code": "SAVE10", "discount_type": "percent", "discount_value": 10, "max_discount": 500},
    {"code": "FLAT500", "discount_type": "fixed", "discount_value": 500, "max_discount": None},
    {"code": "WELCOME", "discount_type": "fixed", "discount_value": 200, "max_discount": None},
]


def seed(db: Session) -> None:
    existing = db.query(Flight).count()
    if existing != len(FLIGHTS_DATA):
        # Re-sync: delete all and re-insert whenever the dataset size changes
        db.query(Flight).delete()
        for f in FLIGHTS_DATA:
            db.add(Flight(**f))
        print(f"Seeded {len(FLIGHTS_DATA)} flights (was {existing})")

    if db.query(Hotel).count() == 0:
        for h in HOTELS_DATA:
            rooms = h.pop("rooms")
            hotel = Hotel(**h)
            db.add(hotel)
            for r in rooms:
                db.add(Room(hotel_id=h["id"], **r))
        print(f"Seeded {len(HOTELS_DATA)} hotels")

    if db.query(Wallet).count() == 0:
        db.add(Wallet(user_id="default", balance=5000))
        print("Seeded default wallet (₹5000)")

    if db.query(Promo).count() == 0:
        for p in PROMOS_DATA:
            db.add(Promo(**p))
        print(f"Seeded {len(PROMOS_DATA)} promos")

    db.commit()
    print("Seed complete")
