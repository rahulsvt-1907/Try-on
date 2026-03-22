from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.routers.deps import get_current_user
from app.schemas.tryon import MeasurementResponse, RecommendationResponse, TryOnMetadata, TryOnResponse
from app.services.ai_service import AIService, DescriptionService
from app.services.cache import CacheClient
from app.services.measurement_service import MeasurementService
from app.services.recommender_service import StyleRecommenderService
from app.core.config import get_settings

router = APIRouter(prefix='/api', tags=['ai'])
settings = get_settings()
cache = CacheClient(settings.redis_url)
ai_service = AIService(cache)
desc_service = DescriptionService()
recommender_service = StyleRecommenderService()
measurement_service = MeasurementService()

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}


def _allowed(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@router.post('/tryon', response_model=TryOnResponse)
async def try_on(
    clothing_image: UploadFile = File(...),
    avatar_image: UploadFile = File(...),
    clothing_prompt: str = Form(default=''),
    avatar_prompt: str = Form(default=''),
    background_prompt: str = Form(default=''),
    avatar_sex: str = Form(default=''),
    seed: str = Form(default=''),
    _user=Depends(get_current_user),
) -> TryOnResponse:
    if not _allowed(clothing_image.filename or '') or not _allowed(avatar_image.filename or ''):
        raise HTTPException(status_code=400, detail='Images must be jpg/jpeg/png/webp')

    clothing_bytes = await clothing_image.read()
    avatar_bytes = await avatar_image.read()
    if len(clothing_bytes) > settings.max_upload_size or len(avatar_bytes) > settings.max_upload_size:
        raise HTTPException(status_code=400, detail='File size exceeds 4MB')

    form_data = {
        k: v
        for k, v in {
            'clothing_prompt': clothing_prompt,
            'avatar_prompt': avatar_prompt,
            'background_prompt': background_prompt,
            'avatar_sex': avatar_sex,
            'seed': seed,
        }.items()
        if v
    }

    image_b64, duration_ms, used_cache = await ai_service.generate_tryon(avatar_bytes, clothing_bytes, form_data)
    description = await desc_service.generate_description(clothing_prompt or 'the selected look', background_prompt)
    return TryOnResponse(image_base64=image_b64, description=description, metadata=TryOnMetadata(duration_ms=duration_ms, used_cache=used_cache))


@router.get('/recommend/{item_id}', response_model=RecommendationResponse)
async def recommend(item_id: int, db: AsyncSession = Depends(get_db)) -> RecommendationResponse:
    recs = await recommender_service.recommend(db, item_id)
    return RecommendationResponse(source_item_id=item_id, recommendations=recs)


@router.post('/estimate-size', response_model=MeasurementResponse)
async def estimate_size(front_photo: UploadFile = File(...)) -> MeasurementResponse:
    size, confidence = measurement_service.estimate_size(await front_photo.read())
    return MeasurementResponse(estimated_size=size, confidence=confidence)
