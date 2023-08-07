from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from models import Medication


def get_medications_keyboard(medications: list[Medication]) -> InlineKeyboardMarkup:
    k = InlineKeyboardMarkup()

    for m in medications:
        k.add(InlineKeyboardButton(f"{m.name} ({m.notification_time})", callback_data=f"{m.id}_btn"))

    return k
