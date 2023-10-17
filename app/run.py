from logging.config import dictConfig

from aiogram import types, Dispatcher, Bot
from aiogram.utils.exceptions import InvalidQueryID
from beanie import init_beanie
from fastapi import FastAPI

from app.bot import dp, bot
from app.config import settings
from app.log_config import log_config
from app.loggers import run_log as logger
from app.models import __beanie_models__
from app.mongo_client import mongo_client_async
from app.scheduler import init_scheduler
from app.exception_handlers import invalid_query_id_exception_handler

dictConfig(log_config)


app = FastAPI(
    title="Medication reminder app",
    description="Send notifications about medications.",
    version="0.0.1",
    docs_url="/api/v1/docs",
)

app.add_exception_handler(InvalidQueryID, invalid_query_id_exception_handler)


@app.on_event("startup")
async def on_startup():
    logger.info("On startup things.")
    webhook_info = await bot.get_webhook_info()
    logger.info(f"webhook_info: {webhook_info}.")

    webhook_url = settings.telegram_webhook_url()
    if webhook_info.url != webhook_url:
        assert await bot.set_webhook(url=webhook_url) is True, "Result of `set_webhook` has to be `True`."
        webhook_info = await bot.get_webhook_info()
        logger.info(f"webhook_info updated: {webhook_info}.")

    await init_beanie(database=mongo_client_async[settings.mongo_db_name], document_models=__beanie_models__)

    # Below import is required because handlers for commands and buttons has to be loaded.
    # Otherwise, sending commands and pushing on buttons will result in nothing.
    import app.handlers  # noqa: F401

    await init_scheduler()


@app.post(settings.telegram_webhook_path(), include_in_schema=False)
async def bot_webhook(update: dict):
    logger.info(f"Update object: {update}.")
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("On shutdown things.")
    session = await bot.get_session()
    await session.close()
