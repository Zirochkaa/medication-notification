import motor.motor_asyncio

from config import settings


mongo_client = motor.motor_asyncio.AsyncIOMotorClient(settings.database_url)
