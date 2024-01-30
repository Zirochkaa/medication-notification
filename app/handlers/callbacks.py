from aiogram import types

from app.bot import bot, dp
from app.config import settings
from app.handlers.callback_data import (
    med_list, med_info, med_delete, med_delete_confirm, med_take_confirm_original, med_take_confirm_followup
)
from app.helpers import DATE_FORMAT
from app.keyboards import (
    get_medication_info_keyboard,
    get_medication_list_keyboard,
    get_medication_delete_confirmation_keyboard,
    get_medication_delete_finish_keyboard,
)
from app.loggers import handlers_callbacks_log as logger
from app.logs_notifications import notification_medication_taken
from app.models import Medication, Notification
from app.texts import (
    medication_info_text,
    medication_delete_confirm_text, medication_delete_finish_text,
    mymedication_empty_text, mymedication_text,
    medication_take_finish_text,
    medication_no_longer_available_text,
)


@dp.callback_query_handler(med_list.filter())
async def med_list_callback(callback: types.CallbackQuery):
    medications = await Medication.get_medications(tg_user_id=callback.from_user.id)

    if not medications:
        await callback.message.edit_text(text=mymedication_empty_text)
    else:
        await callback.message.edit_text(text=mymedication_text,
                                         reply_markup=get_medication_list_keyboard(medications))


@dp.callback_query_handler(med_info.filter())
async def med_info_callback(callback: types.CallbackQuery, callback_data: dict):
    medication = await Medication.get(callback_data["medication_id"])
    if not medication:
        await callback.message.edit_text(medication_no_longer_available_text)
        return

    text = medication_info_text.format(name=medication.name, time=medication.notification_time)
    await callback.message.edit_text(text=text, reply_markup=get_medication_info_keyboard(str(medication.id)))


@dp.callback_query_handler(med_delete.filter())
async def med_delete_callback(callback: types.CallbackQuery, callback_data: dict):
    medication = await Medication.get(callback_data["medication_id"])
    if not medication:
        await callback.message.edit_text(medication_no_longer_available_text)
        return

    text = medication_delete_confirm_text.format(name=medication.name, time=medication.notification_time)
    await callback.message.edit_text(text=text,
                                     reply_markup=get_medication_delete_confirmation_keyboard(str(medication.id)))


@dp.callback_query_handler(med_delete_confirm.filter())
async def med_delete_confirm_callback(callback: types.CallbackQuery, callback_data: dict):
    medication = await Medication.get(callback_data["medication_id"])
    if not medication:
        await callback.message.edit_text(medication_no_longer_available_text)
        return

    await medication.set({Medication.deleted: True})

    logger.info(f"Medication `{medication.name}` was deleted - {medication.id}.")

    text = medication_delete_finish_text.format(name=medication.name, time=medication.notification_time)
    await callback.message.edit_text(text, reply_markup=get_medication_delete_finish_keyboard())


@dp.callback_query_handler(med_take_confirm_original.filter())
async def med_take_confirm_original_callback(callback: types.CallbackQuery, callback_data: dict):
    logger.info(f"Received confirmation callback for ORIGINAL `{callback_data['notification_id']}` notification.")

    await callback.answer("Ok")

    notification = await Notification.get(callback_data["notification_id"], fetch_links=True)
    if not notification:
        await callback.message.edit_text(medication_no_longer_available_text)
        return

    await notification.set({Notification.was_taken: True})

    text = medication_take_finish_text.format(name=notification.medication.name,
                                              date=notification.sent_at.strftime(DATE_FORMAT))

    # Update original notification.
    if notification.tg_original_notification_id and not notification.tg_original_notification_updated:
        await notification.set({Notification.tg_original_notification_updated: True})
        await callback.message.edit_text(text)

    # Update followup notification.
    if notification.tg_followup_notification_id and not notification.tg_followup_notification_updated:
        await notification.set({Notification.tg_followup_notification_updated: True})
        await bot.edit_message_text(text, chat_id=notification.medication.user.tg_chat_id,
                                    message_id=notification.tg_followup_notification_id)

    if settings.telegram_channel_id:
        await notification_medication_taken(notification.medication.user.username, notification.medication.name,
                                            notification.sent_at.strftime(DATE_FORMAT))


@dp.callback_query_handler(med_take_confirm_followup.filter())
async def med_take_confirm_followup_callback(callback: types.CallbackQuery, callback_data: dict):
    logger.info(f"Received confirmation callback for FOLLOWUP `{callback_data['notification_id']}` notification.")

    await callback.answer("Ok")

    notification = await Notification.get(callback_data["notification_id"], fetch_links=True)
    if not notification:
        await callback.message.edit_text(medication_no_longer_available_text)
        return

    await notification.set({Notification.was_taken: True})

    text = medication_take_finish_text.format(name=notification.medication.name,
                                              date=notification.sent_at.strftime(DATE_FORMAT))

    # Update followup notification.
    if notification.tg_followup_notification_id and not notification.tg_followup_notification_updated:
        await notification.set({Notification.tg_followup_notification_updated: True})
        await callback.message.edit_text(text)

    # Update original notification.
    if notification.tg_original_notification_id and not notification.tg_original_notification_updated:
        await notification.set({Notification.tg_original_notification_updated: True})
        await bot.edit_message_text(text, chat_id=notification.medication.user.tg_chat_id,
                                    message_id=notification.tg_original_notification_id)

    if settings.telegram_channel_id:
        await notification_medication_taken(notification.medication.user.username, notification.medication.name,
                                            notification.sent_at.strftime(DATE_FORMAT))
