from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
import os
import logging

from app.backend.services import automation_service
from app.backend.models.account import Account
from app.backend.models.ad import Ad

logger = logging.getLogger(__name__)

# The scheduler instance will be managed by the FastAPI app lifecycle.
scheduler = AsyncIOScheduler()

def initialize_scheduler(client):
    """Initializes and starts the scheduler."""
    if not scheduler.running:
        jobstore = MongoDBJobStore(client=client, database=os.getenv("DB_NAME"))
        scheduler.add_jobstore(jobstore)
        scheduler.start()
        logger.info("Scheduler started and connected to MongoDB job store.")

def shutdown_scheduler():
    """Shuts down the scheduler."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler shut down.")

def schedule_ad_posting_job(schedule_id: str, interval_hours: int, account: Account, ad: Ad):
    """Adds or updates a job in the scheduler."""
    job_id = f"post_ad_{schedule_id}"

    logger.info(f"Scheduling job {job_id} to run every {interval_hours} hours.")

    scheduler.add_job(
        automation_service.post_ad_to_wanuncios,
        'interval',
        hours=interval_hours,
        args=[account, ad],
        id=job_id,
        replace_existing=True,
        misfire_grace_time=3600 # An hour grace time if the scheduler is down
    )

def remove_schedule(schedule_id: str):
    """Removes a job from the scheduler."""
    job_id = f"post_ad_{schedule_id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        logger.info(f"Removed job {job_id} from schedule.")
    else:
        logger.warning(f"Attempted to remove non-existent job: {job_id}")
