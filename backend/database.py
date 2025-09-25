from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "heart_disease_db")

client = None
database = None

async def connect_to_mongo():
    """Create database connection"""
    global client, database
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        database = client[DATABASE_NAME]
        
        # Test connection
        await client.admin.command('ping')
        print("✅ Connected to MongoDB successfully")
        
        # Create indexes
        try:
            await database.doctors.create_index("email", unique=True)
            await database.patients.create_index("email", unique=True)
            await database.predictions.create_index("patient_id")
            await database.audit_logs.create_index("timestamp")
            print("✅ Database indexes created")
        except Exception as e:
            print(f"⚠️ Index creation warning: {e}")
            
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        # For development, we'll continue without MongoDB
        client = None
        database = None

async def close_mongo_connection():
    """Close database connection"""
    global client
    if client:
        client.close()
        print("✅ MongoDB connection closed")

async def get_database():
    """Get database instance"""
    if database is None:
        raise HTTPException(status_code=503, detail="Database not available")
    return database