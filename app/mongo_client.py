import motor.motor_asyncio
import pymongo.mongo_client

from config import settings


mongo_client_async = motor.motor_asyncio.AsyncIOMotorClient(settings.database_url)
mongo_client = pymongo.mongo_client.MongoClient(settings.database_url)
