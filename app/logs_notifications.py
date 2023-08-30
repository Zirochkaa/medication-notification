from app.bot import bot
from app.config import settings
from app.loggers import logs_notifications_log as logger
from app.texts import n_new_user_text, n_medication_taken_text


async def notification_new_user(username: str) -> None:
    logger.info(f"Run `notification_new_user` for @{username} user.")
    await bot.send_message(settings.telegram_channel_id, text=n_new_user_text.format(username=username))


async def notification_medication_taken(username: str, medication_name: str, _date: str) -> None:
    logger.info(f"Run `notification_medication_taken` for @{username} user and "
                f"{medication_name} medication on {_date} date.")
    text = n_medication_taken_text.format(username=username, name=medication_name, date=_date)
    logger.error(text)
    await bot.send_message(settings.telegram_channel_id, text=text)
