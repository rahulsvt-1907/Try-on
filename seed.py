import asyncio
from sqlalchemy import delete

from app.db.session import AsyncSessionLocal, engine
from app.models.base import Base
from app.models.clothing import ClothingItem
from db.pins import pins


def map_pin(pin: dict, idx: int) -> ClothingItem:
    title = pin.get('title') or pin.get('alt') or f'Item {idx + 1}'
    tags = ','.join(filter(None, [pin.get('category', ''), pin.get('gender', ''), *(title.lower().split()[:3])]))
    return ClothingItem(
        name=title[:250],
        category=pin.get('category') or 'Uncategorized',
        gender=pin.get('gender') or 'Unisex',
        image_url=pin.get('src') or '',
        price=39.99 + (idx % 7) * 10,
        tags=tags,
    )


async def seed() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        await session.execute(delete(ClothingItem))
        session.add_all([map_pin(pin, idx) for idx, pin in enumerate(pins)])
        await session.commit()


if __name__ == '__main__':
    asyncio.run(seed())
