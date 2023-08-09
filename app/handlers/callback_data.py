from aiogram.utils.callback_data import CallbackData


med_list = CallbackData("med_list")
med_info = CallbackData("med_info", "medication_id")
med_delete = CallbackData("med_delete", "medication_id")
med_delete_confirm = CallbackData("med_delete_confirm", "medication_id")
