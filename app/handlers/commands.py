from aiogram import types
from aiogram.dispatcher import FSMContext

from app.bot import dp
from app.handlers.states import NewMedicineStatesGroup
from app.helpers import is_time_right_format
from app.keyboards import get_medication_list_keyboard
from app.loggers import handlers_commands_log as logger
from app.models import Medication, User
from app.texts import (
    start_text,
    cancel_text, cancel_empty_text,
    newmedication_choose_name_text, newmedication_choose_time_text,
    newmedication_finish, newmedication_wrong_time_text,
    mymedication_text, mymedication_empty_text,
)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    username = message.from_user.username

    if not await User.find(User.username == username).first_or_none():
        logger.info(f"User @{username} does not exist yet. Creating one ...")
        user = User(username=username, tg_user_id=message.from_user.id, tg_chat_id=message.chat.id)
        result = await user.insert()
        logger.info(f"User @{username} was created - {result.id}.")
    else:
        logger.info(f"User @{username} has already been created.")

    await message.answer(text=start_text.format(username=username))


@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.answer(text=start_text.format(username=message.from_user.username))


@dp.message_handler(commands=["cancel"], state="*")
async def cancel_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(text=cancel_empty_text)
        return

    await message.answer(text=cancel_text)
    await state.finish()


@dp.message_handler(commands=["history"])
async def history_command(message: types.Message):
    await message.answer(text="WIP get a list of last 7 dates when you took your medications.")


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
    await message.answer(text=newmedication_choose_time_text, parse_mode="Markdown")


@dp.message_handler(lambda message: not is_time_right_format(message.text), state=NewMedicineStatesGroup.time)
async def newmedication_command_check_time(message: types.Message):
    logger.error(f"/newmedication check_time:\n{message}\n---")
    await message.answer(text=newmedication_wrong_time_text, parse_mode="Markdown")


@dp.message_handler(state=NewMedicineStatesGroup.time)
async def newmedication_command_load_time(message: types.Message, state: FSMContext):
    logger.error(f"/newmedication load_time:\n{message}\n---")
    async with state.proxy() as data:
        name = data["name"]
        user = await User.find_one(User.tg_user_id == message.from_user.id)
        medication = Medication(name=name, notification_time=message.text, user=user)
        medication = await medication.insert()
        logger.info(f"Medication `{medication.name}` was created - {medication.id}.")

        await message.answer(text=newmedication_finish.format(name=name, time=message.text),
                             parse_mode="Markdown")
    await state.finish()


@dp.message_handler(commands=["mymedication"])
async def mymedication_command(message: types.Message):
    logger.error(f"/mymedication:\n{message}\n---{message.from_user.id}")
    medications = await Medication.get_medications(tg_user_id=message.from_user.id)

    if not medications:
        await message.answer(text=mymedication_empty_text)
    else:
        await message.answer(text=mymedication_text, reply_markup=get_medication_list_keyboard(medications))
