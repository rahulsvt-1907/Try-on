from datetime import datetime
from pydantic import BaseModel, HttpUrl


class ClothingItemCreate(BaseModel):
    name: str
    category: str
    gender: str
    image_url: HttpUrl
    price: float
    tags: str = ''


class ClothingItemResponse(BaseModel):
    id: int
    name: str
    category: str
    gender: str
    image_url: str
    price: float
    tags: str
    created_at: datetime

    model_config = {'from_attributes': True}
