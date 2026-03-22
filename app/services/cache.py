import json
from typing import Any
from loguru import logger

try:
    import redis.asyncio as redis
except Exception:  # pragma: no cover
    redis = None


class CacheClient:
    def __init__(self, redis_url: str):
        self._memory: dict[str, str] = {}
        self._redis = redis.from_url(redis_url, decode_responses=True) if redis else None

    async def get(self, key: str) -> Any | None:
        if self._redis:
            try:
                val = await self._redis.get(key)
                if val:
                    return json.loads(val)
            except Exception as exc:
                logger.warning('redis get failed: {}', exc)
        raw = self._memory.get(key)
        return json.loads(raw) if raw else None

    async def set(self, key: str, value: Any, ex: int = 3600) -> None:
        payload = json.dumps(value)
        if self._redis:
            try:
                await self._redis.set(key, payload, ex=ex)
                return
            except Exception as exc:
                logger.warning('redis set failed: {}', exc)
        self._memory[key] = payload
