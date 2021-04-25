import pytest

@pytest.mark.asyncio
async def test_db_connection():
    from app.db import DATABASE_URL
    import motor.motor_asyncio

    db_connection = motor.motor_asyncio.AsyncIOMotorClient(
        DATABASE_URL, uuidRepresentation="standard"
    )
    await db_connection["test"].test_collection.find_one()
    db_connection.close()