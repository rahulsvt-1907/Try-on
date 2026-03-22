from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.clothing import ClothingItem

router = APIRouter(tags=['pages'])
templates = Jinja2Templates(directory='templates')


@router.get('/', response_class=HTMLResponse)
async def index(request: Request, db: AsyncSession = Depends(get_db)):
    pins = (await db.execute(select(ClothingItem))).scalars().all()
    categories = sorted({pin.category for pin in pins if pin.category})
    return templates.TemplateResponse('index.html', {'request': request, 'pins': pins, 'categories': categories})


@router.get('/tryon', response_class=HTMLResponse)
async def tryon_page(request: Request):
    return templates.TemplateResponse('tryon.html', {'request': request})


@router.get('/health')
async def health() -> dict[str, str]:
    return {'status': 'ok'}


@router.get('/metrics')
async def metrics(db: AsyncSession = Depends(get_db)) -> dict[str, int]:
    total_items = (await db.execute(select(func.count(ClothingItem.id)))).scalar_one()
    return {'catalog_items_total': total_items}
