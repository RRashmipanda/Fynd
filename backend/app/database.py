from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb+srv://rrashmipanda458_db_user:2j5PljhifqLmccwH@cluster0.nwfz5xj.mongodb.net/")
db = client.task_manager
