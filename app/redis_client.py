"""Redis client for cache and confirmations log."""

import json
from typing import Any

import redis
from app.config import (
    REDIS_URL,
    CACHE_TTL_SECONDS,
    REDIS_KEY_CONFIRMATIONS_LOG,
    REDIS_CONFIRMATIONS_LOG_MAXLEN,
)

_redis = None


def get_redis():
    global _redis
    if _redis is not None:
        return _redis
    try:
        _redis = redis.from_url(REDIS_URL, decode_responses=True)
        _redis.ping()
        return _redis
    except Exception:
        _redis = None
        return None


def cache_get(key: str):
    r = get_redis()
    if not r:
        return None
    try:
        raw = r.get(key)
        if raw is None:
            return None
        return json.loads(raw)
    except Exception:
        return None


def cache_set(key: str, value: Any, ttl_seconds: int = None) -> bool:
    r = get_redis()
    if not r:
        return False
    ttl = ttl_seconds or CACHE_TTL_SECONDS
    try:
        r.setex(key, ttl, json.dumps(value, default=str))
        return True
    except Exception:
        return False


def confirmations_log_append(entry: dict) -> bool:
    r = get_redis()
    if not r:
        return False
    try:
        r.lpush(REDIS_KEY_CONFIRMATIONS_LOG, json.dumps(entry, default=str))
        r.ltrim(REDIS_KEY_CONFIRMATIONS_LOG, 0, REDIS_CONFIRMATIONS_LOG_MAXLEN - 1)
        return True
    except Exception:
        return False


def confirmations_log_recent(limit: int = 10) -> list:
    r = get_redis()
    if not r:
        return []
    try:
        raw_list = r.lrange(REDIS_KEY_CONFIRMATIONS_LOG, 0, limit - 1)
        out = []
        for raw in raw_list or []:
            try:
                out.append(json.loads(raw))
            except Exception:
                pass
        return out
    except Exception:
        return []


def close_redis() -> None:
    global _redis
    if _redis:
        try:
            _redis.close()
        except Exception:
            pass
        _redis = None
