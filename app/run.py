from logging.config import dictConfig

from aiogram import types, Dispatcher, Bot
from beanie import init_beanie
from fastapi import FastAPI

from config import settings
from bot import dp, bot
from log_config import log_config
from loggers import run_log
from models import __beanie_models__
from mongo_client import mongo_client


dictConfig(log_config)


app = FastAPI(
    title="Medication reminder app",
    description="Send notifications about medications.",
    version="0.0.1",
    docs_url="/api/v1/docs",
)


@app.on_event("startup")
async def on_startup():
    run_log.info("On startup things.")
    webhook_info = await bot.get_webhook_info()
    run_log.info(f"webhook_info: {webhook_info}.")

    webhook_url = settings.telegram_webhook_url()
    if webhook_info.url != webhook_url:
        assert await bot.set_webhook(url=webhook_url) is True, "Result of `set_webhook` has to be `True`."

    await init_beanie(database=mongo_client[settings.mongo_db_name], document_models=__beanie_models__)

    # Below import is required because handlers for commands and buttons has to be loaded.
    # Otherwise, sending commands and pushing on buttons will result in nothing.
    import handlers  # noqa: F401


@app.post(settings.telegram_webhook_path(), include_in_schema=False)
async def bot_webhook(update: dict):
    run_log.info(f"Update object: {update}.")
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


@app.on_event("shutdown")
async def on_shutdown():
    run_log.info("On shutdown things.")
    session = await bot.get_session()
    await session.close()
