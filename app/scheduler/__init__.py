from datetime import timezone

from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import settings
from app.mongo_client import mongo_client


async def init_scheduler() -> None:
    from app.scheduler.tasks import check_notifications, send_followup_notifications

    jobstores = {"default": MongoDBJobStore(database=settings.mongo_db_name, client=mongo_client)}
    executors = {"default": AsyncIOExecutor()}

    scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors, timezone=timezone.utc)

    scheduler.add_job(check_notifications, "interval", id="check_for_notifications",
                      minutes=1, replace_existing=True)
    scheduler.add_job(send_followup_notifications, "cron", id="send_followup_notifications",
                      hour=20, minute=15, replace_existing=True)

    scheduler.start()
