from aiogram.utils.exceptions import InvalidQueryID
from fastapi import Request

from app.loggers import exception_handlers_log as logger


async def invalid_query_id_exception_handler(request: Request, exc: InvalidQueryID) -> None:
    logger.error(f"InvalidQueryID exception occurred:\n{exc}")
