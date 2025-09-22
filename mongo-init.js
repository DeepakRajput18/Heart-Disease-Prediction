// MongoDB initialization script
db = db.getSiblingDB('heart_disease_db');

// Create collections
db.createCollection('doctors');
db.createCollection('patients');
db.createCollection('predictions');
db.createCollection('audit_logs');
db.createCollection('files');

// Create indexes
db.doctors.createIndex({ "email": 1 }, { unique: true });
db.patients.createIndex({ "email": 1 }, { unique: true });
db.patients.createIndex({ "created_at": 1 });
db.predictions.createIndex({ "patient_id": 1 });
db.predictions.createIndex({ "created_at": 1 });
db.predictions.createIndex({ "risk_level": 1 });
db.audit_logs.createIndex({ "timestamp": 1 });
db.audit_logs.createIndex({ "doctor_id": 1 });
db.files.createIndex({ "patient_id": 1 });

print('Database initialized successfully');