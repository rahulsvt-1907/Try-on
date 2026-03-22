from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.clothing import ClothingItem
from app.schemas.clothing import ClothingItemCreate, ClothingItemResponse

router = APIRouter(prefix='/api/clothing', tags=['clothing'])
templates = Jinja2Templates(directory='templates')


@router.get('', response_model=list[ClothingItemResponse])
async def list_clothing(
    gender: str | None = Query(default=None),
    category: str | None = Query(default=None),
    q: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[ClothingItem]:
    stmt = select(ClothingItem)
    if gender and gender != 'All':
        stmt = stmt.where(ClothingItem.gender == gender)
    if category and category != 'All':
        stmt = stmt.where(ClothingItem.category == category)
    if q:
        stmt = stmt.where(ClothingItem.name.ilike(f'%{q}%'))
    return list((await db.execute(stmt)).scalars().all())


@router.get('/{item_id}', response_model=ClothingItemResponse)
async def get_clothing(item_id: int, db: AsyncSession = Depends(get_db)) -> ClothingItem:
    item = (await db.execute(select(ClothingItem).where(ClothingItem.id == item_id))).scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    return item


@router.post('', response_model=ClothingItemResponse)
async def create_clothing(payload: ClothingItemCreate, db: AsyncSession = Depends(get_db)) -> ClothingItem:
    item = ClothingItem(**payload.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.get('/fragment/grid', response_class=HTMLResponse)
async def clothing_grid_fragment(request: Request, gender: str = 'All', category: str = 'All', q: str = '', db: AsyncSession = Depends(get_db)):
    items = await list_clothing(gender=gender, category=category, q=q, db=db)
    return templates.TemplateResponse('partials/pins_grid.html', {'request': request, 'pins': items})
