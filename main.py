from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.logging import configure_logging
from app.db.session import engine
from app.models.base import Base
from app.routers import auth, clothing, pages, tryon

configure_logging()
app = FastAPI(title='Stylish AI', version='2.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(clothing.router)
app.include_router(tryon.router)


@app.on_event('startup')
async def startup_event() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
