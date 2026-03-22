from __future__ import annotations

import numpy as np
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.clothing import ClothingItem

try:
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover
    SentenceTransformer = None


class StyleRecommenderService:
    def __init__(self) -> None:
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2') if SentenceTransformer else None

    async def recommend(self, session: AsyncSession, source_item_id: int, top_k: int = 3) -> list[int]:
        items = (await session.execute(select(ClothingItem))).scalars().all()
        by_id = {item.id: item for item in items}
        source = by_id.get(source_item_id)
        if not source:
            return []

        texts = [f'{i.name} {i.category} {i.gender} {i.tags}' for i in items]
        if self.model:
            vectors = self.model.encode(texts)
            source_vec = vectors[list(by_id.keys()).index(source_item_id)]
            sims = [float(np.dot(source_vec, v) / (np.linalg.norm(source_vec) * np.linalg.norm(v) + 1e-9)) for v in vectors]
        else:
            logger.warning('sentence-transformers unavailable, using lexical fallback')
            source_tokens = set(texts[list(by_id.keys()).index(source_item_id)].lower().split())
            sims = [len(source_tokens.intersection(set(t.lower().split()))) for t in texts]

        ranked = [item.id for item, _ in sorted(zip(items, sims), key=lambda x: x[1], reverse=True) if item.id != source_item_id]
        return ranked[:top_k]
