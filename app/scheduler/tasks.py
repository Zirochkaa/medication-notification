from datetime import datetime

from loggers import tasks_log as logger
from models import User, Notification
from scheduler.helpers import check_notifications_for_user, send_followup_notification


async def check_notifications() -> None:
    logger.info(f"Run TASK `check_for_notifications` at {datetime.now()}.")

    for user in await User.find_all().to_list():
        await check_notifications_for_user(user)


async def send_followup_notifications() -> None:
    _date = datetime.now()

    logger.info(f"Run TASK `send_followup_notifications` at {_date}.")

    for notification in await Notification.get_current_day_not_taken_notifications(_date):
        await send_followup_notification(notification)
