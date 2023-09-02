from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.mongo_client import MongoClient

from app.config import settings


mongo_client_async: AsyncIOMotorClient = AsyncIOMotorClient(settings.database_url)
mongo_client: MongoClient = MongoClient(settings.database_url)
