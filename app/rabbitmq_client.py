"""RabbitMQ producer and consumer for booking confirmation flow."""

import asyncio
import json
from typing import Any

import aio_pika
from aio_pika import Message
from app.config import RABBITMQ_URL, RABBITMQ_QUEUE_CONFIRMATIONS
from app.redis_client import confirmations_log_append

_connection: aio_pika.RobustConnection | None = None
_channel: aio_pika.Channel | None = None
_consumer_task: asyncio.Task | None = None


async def _ensure_channel() -> aio_pika.Channel | None:
    global _connection, _channel
    if _channel is not None and not _channel.is_closed:
        return _channel
    try:
        _connection = await aio_pika.connect_robust(RABBITMQ_URL)
        _channel = await _connection.channel()
        await _channel.set_qos(prefetch_count=1)
        queue = await _channel.declare_queue(RABBITMQ_QUEUE_CONFIRMATIONS, durable=True)
        assert queue.name == RABBITMQ_QUEUE_CONFIRMATIONS
        return _channel
    except Exception:
        return None


async def publish_confirmation_task(payload: dict[str, Any]) -> bool:
    """Publish a booking confirmation task to RabbitMQ (consumed by worker)."""
    channel = await _ensure_channel()
    if not channel:
        return False
    try:
        await channel.default_exchange.publish(
            Message(
                body=json.dumps(payload, default=str).encode("utf-8"),
                content_type="application/json",
            ),
            routing_key=RABBITMQ_QUEUE_CONFIRMATIONS,
        )
        return True
    except Exception:
        return False


async def _consumer_loop() -> None:
    """Consume messages from booking.confirmation queue and log to Redis."""
    while True:
        try:
            channel = await _ensure_channel()
            if not channel:
                await asyncio.sleep(5)
                continue
            queue = await channel.declare_queue(RABBITMQ_QUEUE_CONFIRMATIONS, durable=True)
            async with queue.iterator() as iterator:
                async for message in iterator:
                    async with message.process():
                        try:
                            body = json.loads(message.body.decode("utf-8"))
                            confirmations_log_append(body)
                        except Exception:
                            pass
        except asyncio.CancelledError:
            break
        except Exception:
            await asyncio.sleep(5)


async def start_rabbitmq_consumer() -> None:
    """Start the RabbitMQ consumer in the background."""
    global _consumer_task
    if _consumer_task is not None:
        return
    _consumer_task = asyncio.create_task(_consumer_loop())


def stop_rabbitmq_consumer() -> None:
    global _consumer_task
    if _consumer_task is not None:
        _consumer_task.cancel()
        _consumer_task = None


async def close_rabbitmq() -> None:
    stop_rabbitmq_consumer()
    global _connection, _channel
    if _channel:
        try:
            await _channel.close()
        except Exception:
            pass
        _channel = None
    if _connection:
        try:
            await _connection.close()
        except Exception:
            pass
        _connection = None
