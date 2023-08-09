from aiogram import types

from bot import dp
from handlers.callback_data import med_list, med_info, med_delete, med_delete_confirm
from keyboards import (
    get_medication_info_keyboard,
    get_medication_list_keyboard,
    get_medication_delete_confirmation_keyboard,
    get_medication_delete_finish_keyboard,
)
from loggers import handlers_callbacks_log as logger
from models import Medication
from texts import (
    medication_info_text,
    medication_delete_confirm_text, medication_delete_finish_text,
    mymedication_empty_text, mymedication_text,
)


@dp.callback_query_handler(med_list.filter())
async def med_list_callback(callback: types.CallbackQuery):
    medications = await Medication.get_medications(user_id=callback.from_user.id)

    if not medications:
        await callback.message.edit_text(text=mymedication_empty_text)
    else:
        await callback.message.edit_text(text=mymedication_text,
                                         reply_markup=get_medication_list_keyboard(medications))


@dp.callback_query_handler(med_info.filter())
async def med_info_callback(callback: types.CallbackQuery, callback_data: dict):
    medication = await Medication.get(callback_data["medication_id"])
    text = medication_info_text.format(name=medication.name, time=medication.notification_time)
    await callback.message.edit_text(text=text, parse_mode="Markdown",
                                     reply_markup=get_medication_info_keyboard(medication))


@dp.callback_query_handler(med_delete.filter())
async def med_delete_callback(callback: types.CallbackQuery, callback_data: dict):
    medication = await Medication.get(callback_data["medication_id"])
    text = medication_delete_confirm_text.format(name=medication.name, time=medication.notification_time)
    await callback.message.edit_text(text=text, parse_mode="Markdown",
                                     reply_markup=get_medication_delete_confirmation_keyboard(medication))


@dp.callback_query_handler(med_delete_confirm.filter())
async def med_delete_confirm_callback(callback: types.CallbackQuery, callback_data: dict):
    medication = await Medication.get(callback_data["medication_id"])
    await medication.delete()
    logger.info(f"Medication `{medication.name}` was deleted - {medication.id}.")

    # TODO Delete existing celery task here.

    text = medication_delete_finish_text.format(name=medication.name, time=medication.notification_time)
    await callback.message.edit_text(text, parse_mode="Markdown",
                                     reply_markup=get_medication_delete_finish_keyboard())
