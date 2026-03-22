import pytest

from app.services.ai_service import AIService
from app.services.cache import CacheClient


@pytest.mark.asyncio
async def test_ai_service_cache_hit():
    cache = CacheClient('redis://localhost:6379/0')
    svc = AIService(cache)

    async def fake_call(files, data):
        return b'fake-image-bytes'

    svc._call_tryon = fake_call

    b64_first, _, used_cache_first = await svc.generate_tryon(b'a', b'b', {'x': '1'})
    b64_second, _, used_cache_second = await svc.generate_tryon(b'a', b'b', {'x': '1'})

    assert b64_first == b64_second
    assert used_cache_first is False
    assert used_cache_second is True
