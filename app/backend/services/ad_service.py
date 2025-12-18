from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

from app.backend.models.ad import Ad, AdCreate

async def get_ad(db: AsyncIOMotorDatabase, ad_id: str) -> Ad | None:
    ad = await db.ads.find_one({"id": ad_id})
    if ad:
        return Ad(**ad)
    return None

async def get_ads(db: AsyncIOMotorDatabase, skip: int = 0, limit: int = 100) -> List[Ad]:
    ads_cursor = db.ads.find().skip(skip).limit(limit)
    ads = await ads_cursor.to_list(length=limit)
    return [Ad(**ad) for ad in ads]

async def create_ad(db: AsyncIOMotorDatabase, ad: AdCreate) -> Ad:
    new_ad = Ad(**ad.dict())
    await db.ads.insert_one(new_ad.dict())
    return new_ad

async def update_ad(db: AsyncIOMotorDatabase, ad_id: str, ad_data: dict) -> bool:
    result = await db.ads.update_one({"id": ad_id}, {"$set": ad_data})
    return result.modified_count > 0

async def delete_ad(db: AsyncIOMotorDatabase, ad_id: str) -> bool:
    result = await db.ads.delete_one({"id": ad_id})
    return result.deleted_count > 0
