from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

from app.backend.models.schedule import Schedule, ScheduleCreate

async def get_schedule(db: AsyncIOMotorDatabase, schedule_id: str) -> Schedule | None:
    schedule = await db.schedules.find_one({"id": schedule_id})
    if schedule:
        return Schedule(**schedule)
    return None

async def get_schedules(db: AsyncIOMotorDatabase, skip: int = 0, limit: int = 100) -> List[Schedule]:
    schedules_cursor = db.schedules.find().skip(skip).limit(limit)
    schedules = await schedules_cursor.to_list(length=limit)
    return [Schedule(**schedule) for schedule in schedules]

async def create_schedule(db: AsyncIOMotorDatabase, schedule: ScheduleCreate) -> Schedule:
    # In a real app, next_republish_at would be calculated based on the interval
    from datetime import datetime, timedelta
    new_schedule_data = schedule.dict()
    new_schedule_data["next_republish_at"] = datetime.utcnow() + timedelta(hours=schedule.republish_interval_hours)
    new_schedule = Schedule(**new_schedule_data)
    await db.schedules.insert_one(new_schedule.dict())
    return new_schedule

async def update_schedule(db: AsyncIOMotorDatabase, schedule_id: str, schedule_data: dict) -> bool:
    result = await db.schedules.update_one({"id": schedule_id}, {"$set": schedule_data})
    return result.modified_count > 0

async def delete_schedule(db: AsyncIOMotorDatabase, schedule_id: str) -> bool:
    result = await db.schedules.delete_one({"id": schedule_id})
    return result.deleted_count > 0
