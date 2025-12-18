from fastapi import APIRouter, Depends, HTTPException, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

from app.backend.models.schedule import Schedule, ScheduleCreate, ScheduleUpdate
from app.backend.services import schedule_service, ad_service, account_service, scheduler_service as sched_svc

router = APIRouter()

async def get_database(request: Request) -> AsyncIOMotorDatabase:
    return request.app.mongodb

@router.post("/schedules/", response_model=Schedule, tags=["schedules"])
async def create_schedule_endpoint(schedule: ScheduleCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    new_schedule = await schedule_service.create_schedule(db=db, schedule=schedule)

    ad = await ad_service.get_ad(db=db, ad_id=new_schedule.ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad to schedule not found")

    account = await account_service.get_account(db=db, account_id=ad.account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account for ad not found")

    if new_schedule.is_active:
        sched_svc.schedule_ad_posting_job(
            schedule_id=new_schedule.id,
            interval_hours=new_schedule.republish_interval_hours,
            account=account,
            ad=ad
        )
    return new_schedule

@router.get("/schedules/", response_model=List[Schedule], tags=["schedules"])
async def read_schedules_endpoint(skip: int = 0, limit: int = 100, db: AsyncIOMotorDatabase = Depends(get_database)):
    return await schedule_service.get_schedules(db=db, skip=skip, limit=limit)

@router.get("/schedules/{schedule_id}", response_model=Schedule, tags=["schedules"])
async def read_schedule_endpoint(schedule_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    db_schedule = await schedule_service.get_schedule(db=db, schedule_id=schedule_id)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return db_schedule

@router.patch("/schedules/{schedule_id}", response_model=Schedule, tags=["schedules"])
async def update_schedule_endpoint(schedule_id: str, schedule: ScheduleUpdate, db: AsyncIOMotorDatabase = Depends(get_database)):
    update_data = schedule.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    success = await schedule_service.update_schedule(db=db, schedule_id=schedule_id, schedule_data=update_data)
    if not success:
        raise HTTPException(status_code=404, detail="Schedule not found or no changes made")

    updated_schedule = await schedule_service.get_schedule(db=db, schedule_id=schedule_id)
    if updated_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found after update")

    ad = await ad_service.get_ad(db=db, ad_id=updated_schedule.ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad for schedule not found")
    account = await account_service.get_account(db=db, account_id=ad.account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account for ad not found")

    if updated_schedule.is_active:
        sched_svc.schedule_ad_posting_job(
            schedule_id=updated_schedule.id,
            interval_hours=updated_schedule.republish_interval_hours,
            account=account,
            ad=ad
        )
    else:
        sched_svc.remove_schedule(schedule_id=updated_schedule.id)

    return updated_schedule

@router.delete("/schedules/{schedule_id}", status_code=204, tags=["schedules"])
async def delete_schedule_endpoint(schedule_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    sched_svc.remove_schedule(schedule_id=schedule_id)

    success = await schedule_service.delete_schedule(db=db, schedule_id=schedule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {}
