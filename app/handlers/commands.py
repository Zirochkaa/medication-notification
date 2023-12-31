from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot import dp
from app.config import settings
from app.handlers.states import NewMedicineStatesGroup
from app.helpers import is_time_right_format, subtract_days_from_datetime, dt_time_min, get_dates_between
from app.keyboards import get_medication_list_keyboard
from app.loggers import handlers_commands_log as logger
from app.logs_notifications import notification_new_user
from app.models import Medication, Notification, User
from app.texts import (
    start_text, start_empty_username_text,
    cancel_text, cancel_empty_text,
    history_header_text, history_empty_text, history_whole_day_text,
    history_whole_day_empty_text, history_one_notification_text,
    newmedication_choose_name_text, newmedication_choose_time_text,
    newmedication_finish, newmedication_wrong_time_text,
    mymedication_text, mymedication_empty_text,
)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    logger.error(f"/start:\n{message}\n---")

    if message.from_user.username is None:
        logger.warning(f"User `{message.from_user}` has no username.")
        await message.answer(text=start_empty_username_text)
        return

    username = message.from_user.username

    if not await User.find(User.username == username).first_or_none():
        logger.info(f"User @{username} does not exist yet. Creating one ...")
        user = User(username=username, tg_user_id=message.from_user.id, tg_chat_id=message.chat.id)
        result = await user.insert()
        logger.info(f"User @{username} was created - {result.id}.")

        if settings.telegram_channel_id:
            await notification_new_user(user.username)
    else:
        logger.info(f"User @{username} has already been created.")

    await message.answer(text=start_text.format(username=username, days_amount=settings.history_days_amount))


@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    logger.error(f"/help:\n{message}\n---")

    if message.from_user.username is None:
        logger.warning(f"User `{message.from_user}` has no username.")
        await message.answer(text=start_empty_username_text)
        return

    await message.answer(text=start_text.format(username=message.from_user.username,
                                                days_amount=settings.history_days_amount))


@dp.message_handler(commands=["cancel"], state="*")
async def cancel_command(message: types.Message, state: FSMContext):
    logger.error(f"/cancel:\n{message}\n---")

    current_state = await state.get_state()
    if current_state is None:
        await message.answer(text=cancel_empty_text)
        return

    await message.answer(text=cancel_text)
    await state.finish()


@dp.message_handler(commands=["history"])
async def history_command(message: types.Message):
    logger.error(f"/history:\n{message}\n---")

    end_dt = datetime.now()
    start_dt = dt_time_min(subtract_days_from_datetime(end_dt, settings.history_days_amount))
    notifications = await Notification.get_taken_notifications_for_time_period(
        tg_user_id=message.from_user.id,
        start_dt=start_dt,
        end_dt=end_dt,
    )

    if not notifications:
        text = history_empty_text.format(days_amount=settings.history_days_amount, start_date=start_dt, end_date=end_dt)
        await message.answer(text=text)
        return

    history_dates = get_dates_between(start_dt, end_dt)

    text = ""
    for dt in history_dates:
        content = ""

        for n in notifications:
            if n.sent_at.date() != dt:
                continue

            content += history_one_notification_text.format(name=n.medication.name)

        text += history_whole_day_text.format(date=dt, content=content or history_whole_day_empty_text)

    text = history_header_text.format(
        days_amount=settings.history_days_amount, start_date=start_dt, end_date=end_dt
    ) + text if text else history_empty_text.format(
        days_amount=settings.history_days_amount, start_date=start_dt, end_date=end_dt
    )
    await message.answer(text=text)


@dp.message_handler(commands=["newmedication"])
async def newmedication_command(message: types.Message):
    logger.error(f"/newmedication:\n{message}\n---")
    await NewMedicineStatesGroup.next()
    await message.answer(text=newmedication_choose_name_text)


@dp.message_handler(state=NewMedicineStatesGroup.name)
async def newmedication_command_load_name(message: types.Message, state: FSMContext):
    logger.error(f"/newmedication load_name:\n{message}\n---")
    async with state.proxy() as data:
        data["name"] = message.text

    await NewMedicineStatesGroup.next()
    await message.answer(text=newmedication_choose_time_text)


@dp.message_handler(lambda message: not is_time_right_format(message.text), state=NewMedicineStatesGroup.time)
async def newmedication_command_check_time(message: types.Message):
    logger.error(f"/newmedication check_time:\n{message}\n---")
    await message.answer(text=newmedication_wrong_time_text)


@dp.message_handler(state=NewMedicineStatesGroup.time)
async def newmedication_command_load_time(message: types.Message, state: FSMContext):
    logger.error(f"/newmedication load_time:\n{message}\n---")
    async with state.proxy() as data:
        name = data["name"]
        user = await User.find_one(User.tg_user_id == message.from_user.id)
        medication = Medication(name=name, notification_time=message.text, user=user)
        medication = await medication.insert()
        logger.info(f"Medication `{medication.name}` was created - {medication.id}.")

        await message.answer(text=newmedication_finish.format(name=name, time=message.text))
    await state.finish()


@dp.message_handler(commands=["mymedication"])
async def mymedication_command(message: types.Message):
    logger.error(f"/mymedication:\n{message}\n---")
    medications = await Medication.get_medications(tg_user_id=message.from_user.id)

    if not medications:
        await message.answer(text=mymedication_empty_text)
    else:
        await message.answer(text=mymedication_text, reply_markup=get_medication_list_keyboard(medications))
