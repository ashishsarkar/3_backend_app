"""Unit tests for Redis client helpers (with mocked redis connection)."""
import json
import unittest.mock as mock
import pytest
from app import redis_client


def test_cache_get_returns_none_when_no_redis():
    with mock.patch.object(redis_client, "get_redis", return_value=None):
        assert redis_client.cache_get("key") is None


def test_cache_get_returns_none_on_miss():
    r = mock.Mock()
    r.get.return_value = None
    with mock.patch.object(redis_client, "get_redis", return_value=r):
        assert redis_client.cache_get("key") is None


def test_cache_get_returns_deserialized_value():
    r = mock.Mock()
    r.get.return_value = json.dumps({"x": 1})
    with mock.patch.object(redis_client, "get_redis", return_value=r):
        assert redis_client.cache_get("key") == {"x": 1}


def test_cache_set_returns_false_when_no_redis():
    with mock.patch.object(redis_client, "get_redis", return_value=None):
        assert redis_client.cache_set("key", {"a": 1}) is False


def test_cache_set_calls_setex():
    r = mock.Mock()
    with mock.patch.object(redis_client, "get_redis", return_value=r), \
         mock.patch.object(redis_client, "CACHE_TTL_SECONDS", 300):
        result = redis_client.cache_set("key", {"a": 1})
    assert result is True
    r.setex.assert_called_once()
    call_args = r.setex.call_args[0]
    assert call_args[0] == "key"
    assert call_args[1] == 300
    assert json.loads(call_args[2]) == {"a": 1}


def test_confirmations_log_recent_returns_empty_when_no_redis():
    with mock.patch.object(redis_client, "get_redis", return_value=None):
        assert redis_client.confirmations_log_recent(limit=5) == []


def test_confirmations_log_recent_parses_entries():
    r = mock.Mock()
    r.lrange.return_value = [
        json.dumps({"booking_id": "BK1", "status": "confirmed"}),
        json.dumps({"booking_id": "BK2", "status": "confirmed"}),
    ]
    with mock.patch.object(redis_client, "get_redis", return_value=r):
        out = redis_client.confirmations_log_recent(limit=10)
    assert len(out) == 2
    assert out[0]["booking_id"] == "BK1"
    assert out[1]["booking_id"] == "BK2"
    r.lrange.assert_called_once_with(redis_client.REDIS_KEY_CONFIRMATIONS_LOG, 0, 9)
