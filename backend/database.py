from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "heart_disease_db")

client = None
database = None

async def connect_to_mongo():
    """Create database connection"""
    global client, database
    client = AsyncIOMotorClient(MONGODB_URL)
    database = client[DATABASE_NAME]
    
    # Create indexes
    await database.doctors.create_index("email", unique=True)
    await database.patients.create_index("email", unique=True)
    await database.predictions.create_index("patient_id")
    await database.audit_logs.create_index("timestamp")

async def close_mongo_connection():
    """Close database connection"""
    global client
    if client:
        client.close()

async def get_database():
    """Get database instance"""
    return database