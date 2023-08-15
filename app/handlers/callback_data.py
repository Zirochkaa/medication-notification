from aiogram.utils.callback_data import CallbackData


med_list = CallbackData("med_l")
med_info = CallbackData("med_i", "medication_id")
med_delete = CallbackData("med_d", "medication_id")
med_delete_confirm = CallbackData("med_d_c", "medication_id")
med_take_confirm_original = CallbackData("med_t_c_o", "notification_id")
med_take_confirm_followup = CallbackData("med_t_c_f", "notification_id")
