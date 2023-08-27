import pytest


@pytest.mark.asyncio
async def test_mongo_connection():
    from app.mongo_client import mongo_client_async
    assert await mongo_client_async.server_info(), "Connection to MongoDB has some issues."
