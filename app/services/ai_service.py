import asyncio
import base64
import hashlib
import time
from typing import Any

import httpx
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import get_settings
from app.services.cache import CacheClient

settings = get_settings()


class AIService:
    def __init__(self, cache: CacheClient, concurrency: int = 4):
        self.cache = cache
        self._semaphore = asyncio.Semaphore(concurrency)

    @retry(wait=wait_exponential(multiplier=1, min=1, max=8), stop=stop_after_attempt(3), reraise=True)
    async def _call_tryon(self, files: dict[str, tuple[str, bytes, str]], data: dict[str, str]) -> bytes:
        headers = {'x-rapidapi-key': settings.rapidapi_key, 'x-rapidapi-host': settings.rapidapi_host}
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(settings.rapidapi_url, headers=headers, files=files, data=data)
            if response.status_code >= 400:
                raise httpx.HTTPStatusError('try-on failed', request=response.request, response=response)
            return response.content

    async def generate_tryon(self, avatar_bytes: bytes, clothing_bytes: bytes, form_data: dict[str, str]) -> tuple[str, int, bool]:
        key_base = avatar_bytes + clothing_bytes + str(sorted(form_data.items())).encode('utf-8')
        cache_key = 'tryon:' + hashlib.sha256(key_base).hexdigest()
        cached = await self.cache.get(cache_key)
        if cached:
            return cached['image_base64'], cached['duration_ms'], True

        start = time.perf_counter()
        async with self._semaphore:
            files = {
                'clothing_image': ('clothing.png', clothing_bytes, 'image/png'),
                'avatar_image': ('avatar.png', avatar_bytes, 'image/png'),
            }
            content = await self._call_tryon(files=files, data=form_data)

        image_base64 = base64.b64encode(content).decode('utf-8')
        duration_ms = int((time.perf_counter() - start) * 1000)
        await self.cache.set(cache_key, {'image_base64': image_base64, 'duration_ms': duration_ms})
        logger.info('tryon_call duration_ms={} payload_keys={}', duration_ms, list(form_data.keys()))
        return image_base64, duration_ms, False


class DescriptionService:
    async def generate_description(self, outfit_name: str, background_prompt: str = '') -> str:
        # Open-source / no-key-friendly fallback for demos.
        context = f' with {background_prompt}' if background_prompt else ''
        return f'{outfit_name} pairs balanced textures and color contrast{context}. Add minimal accessories for a polished finish.'
