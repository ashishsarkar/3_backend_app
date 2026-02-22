"""SQLAlchemy ORM models — all tables for the booking platform."""

from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON
)
from sqlalchemy.orm import relationship
from app.database import Base


class Flight(Base):
    __tablename__ = "flights"

    id = Column(String, primary_key=True, index=True)
    origin = Column(String, nullable=False, index=True)
    origin_city = Column(String, nullable=False)
    destination = Column(String, nullable=False, index=True)
    destination_city = Column(String, nullable=False)
    departure_time = Column(String, nullable=False)
    arrival_time = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    airline = Column(String, nullable=False)
    duration = Column(String, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "origin": self.origin,
            "originCity": self.origin_city,
            "destination": self.destination,
            "destinationCity": self.destination_city,
            "departureTime": self.departure_time,
            "arrivalTime": self.arrival_time,
            "price": self.price,
            "airline": self.airline,
            "duration": self.duration,
        }


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False, index=True)
    address = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    price = Column(Float, nullable=False)
    rating = Column(Float, nullable=True)
    image = Column(String, nullable=True)
    amenities = Column(JSON, nullable=True)

    rooms = relationship("Room", back_populates="hotel", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "address": self.address,
            "lat": self.lat,
            "lng": self.lng,
            "price": self.price,
            "rating": self.rating,
            "image": self.image,
            "amenities": self.amenities or [],
            "rooms": [r.to_dict() for r in self.rooms],
        }


class Room(Base):
    __tablename__ = "rooms"

    id = Column(String, primary_key=True)
    hotel_id = Column(String, ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    max_guests = Column(Integer, nullable=True)

    hotel = relationship("Hotel", back_populates="rooms")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "maxGuests": self.max_guests,
        }


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String, primary_key=True, index=True)
    status = Column(String, nullable=False, default="confirmed")
    type = Column(String, nullable=False, default="flight")
    flight_json = Column(JSON, nullable=True)
    hotel_json = Column(JSON, nullable=True)
    total = Column(Float, nullable=True)
    promo_json = Column(JSON, nullable=True)
    insurance = Column(Boolean, nullable=True, default=False)
    use_wallet = Column(Boolean, nullable=True, default=False)
    wallet_deduction = Column(Float, nullable=True, default=0)
    card_number = Column(String, nullable=True)
    expiry = Column(String, nullable=True)
    refund_status = Column(String, nullable=True)
    refund_initiated_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "type": self.type,
            "flight": self.flight_json,
            "hotel": self.hotel_json,
            "total": self.total,
            "promo": self.promo_json,
            "insurance": self.insurance,
            "useWallet": self.use_wallet,
            "walletDeduction": self.wallet_deduction,
            "refundStatus": self.refund_status,
            "refundInitiatedAt": self.refund_initiated_at.isoformat() if self.refund_initiated_at else None,
            "createdAt": self.created_at.isoformat() + "Z" if self.created_at else None,
        }


class Wallet(Base):
    __tablename__ = "wallet"

    user_id = Column(String, primary_key=True, index=True)
    balance = Column(Float, nullable=False, default=0)


class Promo(Base):
    __tablename__ = "promos"

    code = Column(String, primary_key=True, index=True)
    discount_type = Column(String, nullable=False)  # 'percent' or 'fixed'
    discount_value = Column(Float, nullable=False)
    max_discount = Column(Float, nullable=True)

    def calc_savings(self, amount: float) -> float:
        if self.discount_type == "percent":
            savings = amount * self.discount_value / 100
            return round(min(savings, self.max_discount) if self.max_discount else savings)
        return round(min(self.discount_value, amount))
