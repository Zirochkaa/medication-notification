from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config import settings

storage = MemoryStorage()
bot = Bot(token=settings.telegram_bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
