from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.handlers.callback_data import (
    med_list, med_info, med_delete, med_delete_confirm, med_take_confirm_original, med_take_confirm_followup
)
from app.models import Medication


def get_medication_list_keyboard(medications: list[Medication]) -> InlineKeyboardMarkup:
    """
    Generate a keyboard for list of medications. Each medication is separate button.
    """
    k = InlineKeyboardMarkup()

    for m in medications:
        k.add(InlineKeyboardButton(f"{m.name} ({m.notification_time})", callback_data=med_info.new(m.id)))

    return k


def get_medication_info_keyboard(medication_id: str) -> InlineKeyboardMarkup:
    """
    Generate a keyboard for medication info.
    """
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton("Delete Medication", callback_data=med_delete.new(medication_id)))
    k.add(InlineKeyboardButton("<< Back to Medications List", callback_data=med_list.new()))
    return k


def get_medication_delete_confirmation_keyboard(medication_id: str) -> InlineKeyboardMarkup:
    """
    Generate a keyboard for medication deletion confirmation.
    """
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton("No", callback_data=med_info.new(medication_id)))
    k.add(InlineKeyboardButton("Nope, nevermind", callback_data=med_info.new(medication_id)))
    k.add(InlineKeyboardButton("Yes, delete the medication", callback_data=med_delete_confirm.new(medication_id)))
    k.add(InlineKeyboardButton("<< Back to Medication", callback_data=med_info.new(medication_id)))
    return k


def get_medication_delete_finish_keyboard() -> InlineKeyboardMarkup:
    """
    Generate a keyboard for deleted medication.
    """
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton("<< Back to Medications List", callback_data=med_list.new()))
    return k


def get_medication_take_confirmation_original_keyboard(notification_id: str) -> InlineKeyboardMarkup:
    """
    Generate a keyboard for confirming taking medication for original message.
    """
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton("I took medication",
                               callback_data=med_take_confirm_original.new(notification_id)))
    return k


def get_medication_take_confirmation_followup_keyboard(notification_id: str) -> InlineKeyboardMarkup:
    """
    Generate a keyboard for confirming taking medication for followup message.
    """
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton("I took medication",
                               callback_data=med_take_confirm_followup.new(notification_id)))
    return k
