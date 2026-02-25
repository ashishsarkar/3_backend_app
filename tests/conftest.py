"""
Pytest configuration and fixtures for 3-backend-app.
Sets test DB (SQLite in-memory) and mocks external services so tests run without Redis/Kafka/RabbitMQ.
"""
import os
import unittest.mock as mock

import pytest

# Must set before any app import so database uses SQLite
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory?")

# Prevent RabbitMQ consumer and external connections during tests
_patches = [
    mock.patch("app.rabbitmq_client.start_rabbitmq_consumer", new=mock.AsyncMock(return_value=None)),
    mock.patch("app.rabbitmq_client.close_rabbitmq", new=mock.AsyncMock(return_value=None)),
    mock.patch("app.kafka_client.close_kafka", new=mock.AsyncMock(return_value=None)),
    mock.patch("app.redis_client.close_redis", new=mock.Mock(return_value=None)),
    mock.patch("app.mongodb.ping_mongo", new=mock.AsyncMock(return_value=True)),
]
for p in _patches:
    p.start()

from fastapi.testclient import TestClient
from app.main import app  # noqa: E402

# Now app is loaded with test DATABASE_URL and no real messaging


@pytest.fixture(scope="session")
def client():
    """TestClient for the FastAPI app. Uses in-memory SQLite and mocked Redis/Kafka/RabbitMQ."""
    return TestClient(app)


@pytest.fixture
def db_session(client):
    """Trigger lifespan so DB is created and seeded; yield for tests that need a fresh session."""
    # First request runs lifespan (create_all, seed)
    client.get("/")
    from app.database import SessionLocal
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
