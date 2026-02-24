"""Kafka producer for booking events."""

import json
from typing import Any

from aiokafka import AIOKafkaProducer
from app.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_BOOKING_TOPIC

_producer = None


async def get_kafka_producer():
    global _producer
    if _producer is None:
        try:
            _producer = AIOKafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"),
            )
            await _producer.start()
        except Exception:
            _producer = None
    return _producer


async def publish_booking_event(event_type: str, payload: dict) -> bool:
    producer = await get_kafka_producer()
    if not producer:
        return False
    try:
        msg = {"event": event_type, **payload}
        await producer.send_and_wait(KAFKA_BOOKING_TOPIC, value=msg)
        return True
    except Exception:
        return False


async def close_kafka() -> None:
    global _producer
    if _producer:
        try:
            await _producer.stop()
        except Exception:
            pass
        _producer = None
