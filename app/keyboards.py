from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.callback_data import med_list, med_info, med_delete, med_delete_confirm
from models import Medication


def get_medication_list_keyboard(medications: list[Medication]) -> InlineKeyboardMarkup:
    """
    Generate a keyboard for list of medications. Each medication is separate button.
    """
    k = InlineKeyboardMarkup()

    for m in medications:
        k.add(InlineKeyboardButton(f"{m.name} ({m.notification_time})", callback_data=med_info.new(m.id)))

    return k


def get_medication_info_keyboard(medication: Medication) -> InlineKeyboardMarkup:
    """
    Generate a keyboard for medication info.
    """
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton("Delete Medication", callback_data=med_delete.new(medication.id)))
    k.add(InlineKeyboardButton("<< Back to Medications List", callback_data=med_list.new()))
    return k


def get_medication_delete_confirmation_keyboard(medication: Medication) -> InlineKeyboardMarkup:
    """
    Generate a keyboard for medication deletion confirmation.
    """
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton("No", callback_data=med_info.new(medication.id)))
    k.add(InlineKeyboardButton("Nope, nevermind", callback_data=med_info.new(medication.id)))
    k.add(InlineKeyboardButton("Yes, delete the medication", callback_data=med_delete_confirm.new(medication.id)))
    k.add(InlineKeyboardButton("<< Back to Medication", callback_data=med_info.new(medication.id)))
    return k


def get_medication_delete_finish_keyboard() -> InlineKeyboardMarkup:
    """
    Generate a keyboard for deleted medication.
    """
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton("<< Back to Medications List", callback_data=med_list.new()))
    return k
