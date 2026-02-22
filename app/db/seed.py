"""Seeds the PostgreSQL database on startup if tables are empty."""

from sqlalchemy.orm import Session
from app.models import Flight, Hotel, Room, Wallet, Promo


FLIGHTS_DATA = [
    {
        "id": "f1",
        "origin": "DEL",
        "origin_city": "New Delhi",
        "destination": "BOM",
        "destination_city": "Mumbai",
        "departure_time": "2025-03-15T08:00:00Z",
        "arrival_time": "2025-03-15T10:30:00Z",
        "price": 4500,
        "airline": "Booking Life",
        "duration": "2h 30m",
    },
    {
        "id": "f2",
        "origin": "BOM",
        "origin_city": "Mumbai",
        "destination": "DEL",
        "destination_city": "New Delhi",
        "departure_time": "2025-03-16T14:00:00Z",
        "arrival_time": "2025-03-16T16:30:00Z",
        "price": 5200,
        "airline": "Air India",
        "duration": "2h 30m",
    },
    {
        "id": "f3",
        "origin": "BLR",
        "origin_city": "Bengaluru",
        "destination": "GOI",
        "destination_city": "Goa",
        "departure_time": "2025-03-17T09:00:00Z",
        "arrival_time": "2025-03-17T10:00:00Z",
        "price": 3200,
        "airline": "Booking Life",
        "duration": "1h",
    },
    {
        "id": "f4",
        "origin": "MAA",
        "origin_city": "Chennai",
        "destination": "HYD",
        "destination_city": "Hyderabad",
        "departure_time": "2025-03-18T11:30:00Z",
        "arrival_time": "2025-03-18T12:45:00Z",
        "price": 2800,
        "airline": "SpiceJet",
        "duration": "1h 15m",
    },
    {
        "id": "f5",
        "origin": "DEL",
        "origin_city": "New Delhi",
        "destination": "CCU",
        "destination_city": "Kolkata",
        "departure_time": "2025-03-19T06:00:00Z",
        "arrival_time": "2025-03-19T08:15:00Z",
        "price": 4100,
        "airline": "Vistara",
        "duration": "2h 15m",
    },
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
    if db.query(Flight).count() == 0:
        for f in FLIGHTS_DATA:
            db.add(Flight(**f))
        print(f"Seeded {len(FLIGHTS_DATA)} flights")

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
