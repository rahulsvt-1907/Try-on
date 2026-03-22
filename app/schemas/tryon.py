from pydantic import BaseModel


class TryOnMetadata(BaseModel):
    duration_ms: int
    used_cache: bool


class TryOnResponse(BaseModel):
    image_base64: str
    description: str
    metadata: TryOnMetadata


class RecommendationResponse(BaseModel):
    source_item_id: int
    recommendations: list[int]


class MeasurementResponse(BaseModel):
    estimated_size: str
    confidence: float
