from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config import settings

storage = MemoryStorage()
bot = Bot(token=settings.telegram_bot_token)
dp = Dispatcher(bot, storage=storage)
