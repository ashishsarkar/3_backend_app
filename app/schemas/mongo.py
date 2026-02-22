"""Pydantic schemas for MongoDB collections."""

from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------

class ChatMessage(BaseModel):
    """A single turn in a chat conversation."""
    session_id: str
    role: Literal["user", "assistant"]
    text: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatMessageOut(ChatMessage):
    id: Optional[str] = None


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"


# ---------------------------------------------------------------------------
# Price Alerts
# ---------------------------------------------------------------------------

class PriceAlert(BaseModel):
    """User-defined price alert — triggers when price drops below threshold."""
    user_id: str = "default"
    type: Literal["flight", "hotel"]
    # Flight alert fields
    origin: Optional[str] = None
    destination: Optional[str] = None
    # Hotel alert fields
    location: Optional[str] = None
    # Common
    max_price: float
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    triggered_at: Optional[datetime] = None


class PriceAlertCreate(BaseModel):
    type: Literal["flight", "hotel"]
    origin: Optional[str] = None
    destination: Optional[str] = None
    location: Optional[str] = None
    max_price: float


class PriceAlertOut(PriceAlert):
    id: str


# ---------------------------------------------------------------------------
# Activity Logs
# ---------------------------------------------------------------------------

class ActivityLog(BaseModel):
    """Tracks user actions — search, view, booking events."""
    user_id: str = "default"
    event: Literal["search_flight", "search_hotel", "view_flight", "view_hotel", "booking_created", "booking_cancelled"]
    payload: dict = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ActivityLogCreate(BaseModel):
    event: Literal["search_flight", "search_hotel", "view_flight", "view_hotel", "booking_created", "booking_cancelled"]
    payload: dict = {}


# ---------------------------------------------------------------------------
# User Preferences
# ---------------------------------------------------------------------------

class UserPreferences(BaseModel):
    user_id: str = "default"
    currency: str = "INR"
    theme: Literal["light", "dark"] = "light"
    email_alerts: bool = True
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserPreferencesUpdate(BaseModel):
    currency: Optional[str] = None
    theme: Optional[Literal["light", "dark"]] = None
    email_alerts: Optional[bool] = None
