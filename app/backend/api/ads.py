from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from pydantic import BaseModel

from app.backend.services import ai_service, ad_service, account_service, automation_service
from app.backend.models.ad import Ad, AdCreate, AdUpdate

router = APIRouter()

# Dependency to get the DB connection
async def get_database(request: Request) -> AsyncIOMotorDatabase:
    return request.app.mongodb

class AdTextGenerationRequest(BaseModel):
    prompt: str

@router.post("/ads/generate-text", tags=["ads"])
async def generate_ad_text_endpoint(request: AdTextGenerationRequest):
    generated_text = ai_service.generate_ad_text(request.prompt)
    return {"generated_text": generated_text}


@router.post("/ads/", response_model=Ad, tags=["ads"])
async def create_ad_endpoint(ad: AdCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Check if account exists
    db_account = await account_service.get_account(db=db, account_id=ad.account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail=f"Account with id {ad.account_id} not found")
    return await ad_service.create_ad(db=db, ad=ad)

@router.get("/ads/", response_model=List[Ad], tags=["ads"])
async def read_ads_endpoint(skip: int = 0, limit: int = 100, db: AsyncIOMotorDatabase = Depends(get_database)):
    ads = await ad_service.get_ads(db=db, skip=skip, limit=limit)
    return ads

@router.get("/ads/{ad_id}", response_model=Ad, tags=["ads"])
async def read_ad_endpoint(ad_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    db_ad = await ad_service.get_ad(db=db, ad_id=ad_id)
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Ad not found")
    return db_ad

@router.patch("/ads/{ad_id}", response_model=Ad, tags=["ads"])
async def update_ad_endpoint(ad_id: str, ad: AdUpdate, db: AsyncIOMotorDatabase = Depends(get_database)):
    update_data = ad.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    success = await ad_service.update_ad(db=db, ad_id=ad_id, ad_data=update_data)
    if not success:
        raise HTTPException(status_code=404, detail="Ad not found or no changes made")

    updated_ad = await ad_service.get_ad(db=db, ad_id=ad_id)
    if updated_ad is None:
        raise HTTPException(status_code=404, detail="Ad not found after update")
    return updated_ad

@router.delete("/ads/{ad_id}", status_code=204, tags=["ads"])
async def delete_ad_endpoint(ad_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    success = await ad_service.delete_ad(db=db, ad_id=ad_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ad not found")
    return {}

@router.post("/ads/{ad_id}/publish", tags=["ads"])
async def publish_ad_endpoint(ad_id: str, background_tasks: BackgroundTasks, db: AsyncIOMotorDatabase = Depends(get_database)):
    db_ad = await ad_service.get_ad(db=db, ad_id=ad_id)
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Ad not found")

    db_account = await account_service.get_account(db=db, account_id=db_ad.account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account for this ad not found")

    background_tasks.add_task(automation_service.post_ad_to_wanuncios, db_account, db_ad)

    return {"message": "Ad publishing has been started in the background."}
