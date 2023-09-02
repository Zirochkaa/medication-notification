import pytest
from motor.motor_asyncio import AsyncIOMotorClient


@pytest.mark.asyncio
async def test_mongo_connection(mongodb_client: AsyncIOMotorClient):
    result = await mongodb_client.server_info()
    assert result["ok"] == 1.0, "Connection to MongoDB has some issues."
