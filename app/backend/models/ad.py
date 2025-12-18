from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime

class AdBase(BaseModel):
    title: str
    description: str
    category: str
    subcategory: str
    province: str
    zone: Optional[str] = None
    price: Optional[float] = None
    images: List[str] = []

class AdCreate(AdBase):
    account_id: str

class AdUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    province: Optional[str] = None
    zone: Optional[str] = None
    price: Optional[float] = None
    images: Optional[List[str]] = None

class Ad(AdBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    account_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_published_at: Optional[datetime] = None

    class Config:
        from_attributes = True
