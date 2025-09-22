#!/usr/bin/env python3
"""
Database initialization script for Heart Disease Prediction System
Creates initial admin user and sample data
"""

import asyncio
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

# Database configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "heart_disease_db")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def init_database():
    """Initialize database with admin user and sample data"""
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    print("🔗 Connected to MongoDB")
    
    try:
        # Create indexes
        await create_indexes(db)
        print("📊 Created database indexes")
        
        # Create admin user
        await create_admin_user(db)
        print("👤 Created admin user")
        
        # Create sample doctor
        await create_sample_doctor(db)
        print("🩺 Created sample doctor")
        
        print("✅ Database initialization completed successfully!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
    finally:
        client.close()

async def create_indexes(db):
    """Create database indexes for better performance"""
    
    # Doctors collection indexes
    await db.doctors.create_index("email", unique=True)
    
    # Patients collection indexes
    await db.patients.create_index("email", unique=True)
    await db.patients.create_index("created_at")
    
    # Predictions collection indexes
    await db.predictions.create_index("patient_id")
    await db.predictions.create_index("created_at")
    await db.predictions.create_index("risk_level")
    
    # Audit logs collection indexes
    await db.audit_logs.create_index("timestamp")
    await db.audit_logs.create_index("doctor_id")
    await db.audit_logs.create_index("patient_id")
    
    # Files collection indexes
    await db.files.create_index("patient_id")
    await db.files.create_index("uploaded_at")

async def create_admin_user(db):
    """Create default admin user"""
    
    admin_email = "admin@heartpredict.com"
    admin_password = "admin123"  # Change this in production!
    
    # Check if admin already exists
    existing_admin = await db.doctors.find_one({"email": admin_email})
    if existing_admin:
        print(f"⚠️  Admin user already exists: {admin_email}")
        return
    
    # Create admin user
    admin_user = {
        "name": "System Administrator",
        "email": admin_email,
        "password_hash": pwd_context.hash(admin_password),
        "role": "admin",
        "specialization": "System Administration",
        "phone": "+1-555-0100",
        "created_at": datetime.utcnow()
    }
    
    await db.doctors.insert_one(admin_user)
    print(f"✅ Admin user created: {admin_email} / {admin_password}")

async def create_sample_doctor(db):
    """Create sample doctor for testing"""
    
    doctor_email = "dr.smith@heartpredict.com"
    doctor_password = "doctor123"  # Change this in production!
    
    # Check if doctor already exists
    existing_doctor = await db.doctors.find_one({"email": doctor_email})
    if existing_doctor:
        print(f"⚠️  Sample doctor already exists: {doctor_email}")
        return
    
    # Create sample doctor
    doctor_user = {
        "name": "Dr. John Smith",
        "email": doctor_email,
        "password_hash": pwd_context.hash(doctor_password),
        "role": "doctor",
        "specialization": "Cardiology",
        "phone": "+1-555-0101",
        "created_at": datetime.utcnow()
    }
    
    await db.doctors.insert_one(doctor_user)
    print(f"✅ Sample doctor created: {doctor_email} / {doctor_password}")

async def create_sample_patients(db):
    """Create sample patients for testing"""
    
    sample_patients = [
        {
            "name": "Alice Johnson",
            "email": "alice.johnson@email.com",
            "phone": "+1-555-0201",
            "date_of_birth": datetime(1985, 3, 15),
            "gender": "female",
            "address": "123 Main St, Anytown, ST 12345",
            "emergency_contact": "Bob Johnson - +1-555-0202",
            "medical_history": "No significant medical history",
            "created_at": datetime.utcnow(),
            "created_by": "admin@heartpredict.com"
        },
        {
            "name": "Robert Davis",
            "email": "robert.davis@email.com",
            "phone": "+1-555-0203",
            "date_of_birth": datetime(1970, 8, 22),
            "gender": "male",
            "address": "456 Oak Ave, Somewhere, ST 67890",
            "emergency_contact": "Mary Davis - +1-555-0204",
            "medical_history": "Hypertension, managed with medication",
            "created_at": datetime.utcnow(),
            "created_by": "admin@heartpredict.com"
        },
        {
            "name": "Sarah Wilson",
            "email": "sarah.wilson@email.com",
            "phone": "+1-555-0205",
            "date_of_birth": datetime(1992, 12, 5),
            "gender": "female",
            "address": "789 Pine Rd, Elsewhere, ST 54321",
            "emergency_contact": "Tom Wilson - +1-555-0206",
            "medical_history": "Family history of heart disease",
            "created_at": datetime.utcnow(),
            "created_by": "dr.smith@heartpredict.com"
        }
    ]
    
    for patient in sample_patients:
        existing = await db.patients.find_one({"email": patient["email"]})
        if not existing:
            await db.patients.insert_one(patient)
            print(f"✅ Created sample patient: {patient['name']}")

if __name__ == "__main__":
    print("🚀 Initializing Heart Disease Prediction Database...")
    asyncio.run(init_database())