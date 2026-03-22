import asyncio
import json
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.session import get_db
from app.models.base import Base
from app.models.clothing import ClothingItem
from app.models.user import User
from app.services.auth_service import hash_password
from main import app

TEST_DB_URL = 'sqlite+aiosqlite:///./test_stylish_ai.db'


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def db_session():
    engine = create_async_engine(TEST_DB_URL, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    session_local = async_sessionmaker(engine, expire_on_commit=False)
    async with session_local() as session:
        session.add(User(email='demo@example.com', full_name='Demo', hashed_password=hash_password('password123'), measurements=json.dumps({})))
        session.add(ClothingItem(name='Blue Jacket', category='Jackets', gender='Male', image_url='http://x/y.jpg', price=79.0, tags='blue,jacket'))
        await session.commit()
        yield session
    await engine.dispose()


@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
    app.dependency_overrides.clear()
