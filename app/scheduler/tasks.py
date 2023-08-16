from datetime import datetime

from app.loggers import tasks_log as logger
from app.models import User, Notification
from app.scheduler.helpers import check_notifications_for_user, send_followup_notification


async def check_notifications() -> None:
    logger.info(f"Run TASK `check_for_notifications` at {datetime.now()}.")

    for user in await User.find_all().to_list():
        await check_notifications_for_user(user)


async def send_followup_notifications() -> None:
    _date = datetime.now()

    logger.info(f"Run TASK `send_followup_notifications` at {_date}.")

    for notification in await Notification.get_not_taken_notifications_for_current_day(_date):
        await send_followup_notification(notification)
