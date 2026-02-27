"""App configuration from environment."""

import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://booking_user:booking_pass@localhost:5432/booking")
MONGODB_URL = os.environ.get("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB = os.environ.get("MONGODB_DB", "booking")

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CACHE_TTL_SECONDS = int(os.environ.get("CACHE_TTL_SECONDS", "300"))

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_BOOKING_TOPIC = os.environ.get("KAFKA_BOOKING_TOPIC", "booking.events")

RABBITMQ_URL = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
RABBITMQ_QUEUE_CONFIRMATIONS = os.environ.get("RABBITMQ_QUEUE_CONFIRMATIONS", "booking.confirmation")
REDIS_KEY_CONFIRMATIONS_LOG = "confirmations:log"
REDIS_CONFIRMATIONS_LOG_MAXLEN = 100

ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL", "http://localhost:9200")
ELASTICSEARCH_LOCATIONS_INDEX = "locations"

PORT = int(os.environ.get("PORT", "4000"))
