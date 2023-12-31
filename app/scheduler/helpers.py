from datetime import datetime

from app.bot import bot
from app.helpers import DATE_FORMAT
from app.keyboards import (
    get_medication_take_confirmation_original_keyboard,
    get_medication_take_confirmation_followup_keyboard,
)
from app.loggers import scheduler_helpers_log as logger
from app.models import Medication, Notification, User
from app.texts import medication_take_confirm_text, medication_take_followup_text


async def check_notifications_for_user(user: User) -> None:
    dt = datetime.now()

    logger.info(f"Run `check_notifications_for_user` for `{user.username}` at {dt}.")

    medications = await Medication.get_medications_ready_for_notifications(user.tg_user_id, dt)

    for medication in medications:
        notification = await Notification.get_notification_for_current_day(medication, dt)

        if notification:
            logger.info(f"Notification for `{medication.id}` medication on {dt.date().strftime(DATE_FORMAT)} "
                        f"was already sent at {notification.sent_at}.")
            continue

        await send_initial_notification(user, medication)


async def send_initial_notification(user: User, medication: Medication) -> None:
    logger.info(f"Run `send_initial_notification` for `{user.username}` "
                f"on `{datetime.now().strftime(DATE_FORMAT)}` date.")

    notification = Notification(sent_at=datetime.now(), medication=medication)
    notification = await notification.insert()
    logger.info(f"Notification for `{medication.id}` medication on {notification.sent_at.date()} "
                f"was created - {notification.id}.")

    text = medication_take_confirm_text.format(name=medication.name, date=notification.sent_at.strftime(DATE_FORMAT))
    reply_markup = get_medication_take_confirmation_original_keyboard(str(notification.id))
    message = await bot.send_message(user.tg_chat_id, text=text, reply_markup=reply_markup)

    await notification.set({Notification.tg_original_notification_id: message.message_id})

    logger.info(f"Notification `{notification.id}` was sent at {datetime.now()}.")


async def send_followup_notification(notification: Notification) -> None:
    logger.info(f"Run `send_followup_notification` for `{notification.id}` notification "
                f"on `{datetime.now().strftime(DATE_FORMAT)}` date.")

    text = medication_take_followup_text.format(name=notification.medication.name,
                                                date=notification.sent_at.strftime(DATE_FORMAT))
    reply_markup = get_medication_take_confirmation_followup_keyboard(str(notification.id))
    message = await bot.send_message(notification.medication.user.tg_chat_id, text=text, reply_markup=reply_markup)

    await notification.set({Notification.tg_followup_notification_id: message.message_id})

    logger.info(f"Followup for notification `{notification.id}` was sent at {datetime.now()}.")
