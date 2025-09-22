from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import os
from pathlib import Path

from .auth import get_current_user, create_access_token, verify_password, get_password_hash
from .database import get_database
from .models import *
from .ml_model import HeartDiseasePredictor
from .utils import save_upload_file

app = FastAPI(
    title="Heart Disease Prediction API",
    description="Professional heart disease prediction system for medical professionals",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Security
security = HTTPBearer()

# Initialize ML model
ml_model = HeartDiseasePredictor()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    with open("frontend/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/api/auth/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db=Depends(get_database)):
    """Authenticate doctor and return JWT token"""
    doctor = await db.doctors.find_one({"email": credentials.email})
    if not doctor or not verify_password(credentials.password, doctor["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(data={"sub": doctor["email"], "role": doctor["role"]})
    
    # Log login activity
    await db.audit_logs.insert_one({
        "doctor_id": str(doctor["_id"]),
        "action": "login",
        "timestamp": datetime.utcnow(),
        "ip_address": "unknown"  # In production, get real IP
    })
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        doctor_info=DoctorInfo(
            id=str(doctor["_id"]),
            name=doctor["name"],
            email=doctor["email"],
            role=doctor["role"],
            specialization=doctor.get("specialization", "")
        )
    )

@app.get("/api/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    """Get dashboard statistics"""
    total_patients = await db.patients.count_documents({})
    high_risk_patients = await db.predictions.count_documents({"risk_level": "High Risk"})
    recent_predictions = await db.predictions.count_documents({
        "created_at": {"$gte": datetime.utcnow() - timedelta(days=7)}
    })
    total_predictions = await db.predictions.count_documents({})
    
    return DashboardStats(
        total_patients=total_patients,
        high_risk_patients=high_risk_patients,
        recent_predictions=recent_predictions,
        total_predictions=total_predictions
    )

@app.post("/api/patients", response_model=PatientResponse)
async def create_patient(
    patient: PatientCreate,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    """Create a new patient"""
    patient_dict = patient.dict()
    patient_dict["created_at"] = datetime.utcnow()
    patient_dict["created_by"] = current_user["email"]
    
    result = await db.patients.insert_one(patient_dict)
    
    # Log activity
    await db.audit_logs.insert_one({
        "doctor_id": current_user["email"],
        "action": "create_patient",
        "patient_id": str(result.inserted_id),
        "timestamp": datetime.utcnow()
    })
    
    patient_dict["id"] = str(result.inserted_id)
    return PatientResponse(**patient_dict)

@app.get("/api/patients", response_model=List[PatientResponse])
async def get_patients(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    """Get all patients with pagination"""
    cursor = db.patients.find().skip(skip).limit(limit)
    patients = []
    async for patient in cursor:
        patient["id"] = str(patient["_id"])
        patients.append(PatientResponse(**patient))
    return patients

@app.get("/api/patients/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: str,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    """Get patient by ID"""
    from bson import ObjectId
    patient = await db.patients.find_one({"_id": ObjectId(patient_id)})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient["id"] = str(patient["_id"])
    return PatientResponse(**patient)

@app.put("/api/patients/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: str,
    patient_update: PatientUpdate,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    """Update patient information"""
    from bson import ObjectId
    
    update_data = {k: v for k, v in patient_update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.patients.update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Log activity
    await db.audit_logs.insert_one({
        "doctor_id": current_user["email"],
        "action": "update_patient",
        "patient_id": patient_id,
        "timestamp": datetime.utcnow()
    })
    
    updated_patient = await db.patients.find_one({"_id": ObjectId(patient_id)})
    updated_patient["id"] = str(updated_patient["_id"])
    return PatientResponse(**updated_patient)

@app.delete("/api/patients/{patient_id}")
async def delete_patient(
    patient_id: str,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    """Delete patient"""
    from bson import ObjectId
    
    result = await db.patients.delete_one({"_id": ObjectId(patient_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Log activity
    await db.audit_logs.insert_one({
        "doctor_id": current_user["email"],
        "action": "delete_patient",
        "patient_id": patient_id,
        "timestamp": datetime.utcnow()
    })
    
    return {"message": "Patient deleted successfully"}

@app.post("/api/predictions", response_model=PredictionResponse)
async def create_prediction(
    prediction_data: PredictionCreate,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    """Create heart disease prediction"""
    # Run ML prediction
    clinical_data = [
        prediction_data.age,
        prediction_data.sex,
        prediction_data.cp,
        prediction_data.trestbps,
        prediction_data.chol,
        prediction_data.fbs,
        prediction_data.restecg,
        prediction_data.thalach,
        prediction_data.exang,
        prediction_data.oldpeak,
        prediction_data.slope,
        prediction_data.ca,
        prediction_data.thal
    ]
    
    probability, risk_level = ml_model.predict(clinical_data)
    
    # Save prediction to database
    prediction_dict = prediction_data.dict()
    prediction_dict.update({
        "probability": probability,
        "risk_level": risk_level,
        "created_at": datetime.utcnow(),
        "created_by": current_user["email"]
    })
    
    result = await db.predictions.insert_one(prediction_dict)
    
    # Log activity
    await db.audit_logs.insert_one({
        "doctor_id": current_user["email"],
        "action": "create_prediction",
        "patient_id": prediction_data.patient_id,
        "timestamp": datetime.utcnow()
    })
    
    prediction_dict["id"] = str(result.inserted_id)
    return PredictionResponse(**prediction_dict)

@app.get("/api/predictions/{patient_id}", response_model=List[PredictionResponse])
async def get_patient_predictions(
    patient_id: str,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    """Get all predictions for a patient"""
    cursor = db.predictions.find({"patient_id": patient_id}).sort("created_at", -1)
    predictions = []
    async for prediction in cursor:
        prediction["id"] = str(prediction["_id"])
        predictions.append(PredictionResponse(**prediction))
    return predictions

@app.post("/api/upload/{patient_id}")
async def upload_file(
    patient_id: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    """Upload file for patient"""
    file_path = await save_upload_file(file, patient_id)
    
    # Save file reference in database
    file_doc = {
        "patient_id": patient_id,
        "filename": file.filename,
        "file_path": file_path,
        "content_type": file.content_type,
        "uploaded_at": datetime.utcnow(),
        "uploaded_by": current_user["email"]
    }
    
    result = await db.files.insert_one(file_doc)
    
    # Log activity
    await db.audit_logs.insert_one({
        "doctor_id": current_user["email"],
        "action": "upload_file",
        "patient_id": patient_id,
        "filename": file.filename,
        "timestamp": datetime.utcnow()
    })
    
    return {"message": "File uploaded successfully", "file_id": str(result.inserted_id)}

@app.get("/api/analytics/risk-distribution")
async def get_risk_distribution(
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    """Get risk distribution analytics"""
    pipeline = [
        {"$group": {"_id": "$risk_level", "count": {"$sum": 1}}}
    ]
    
    result = []
    async for doc in db.predictions.aggregate(pipeline):
        result.append({"risk_level": doc["_id"], "count": doc["count"]})
    
    return result

@app.get("/api/analytics/predictions-timeline")
async def get_predictions_timeline(
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    """Get predictions over time"""
    pipeline = [
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$created_at"},
                    "month": {"$month": "$created_at"},
                    "day": {"$dayOfMonth": "$created_at"}
                },
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}}
    ]
    
    result = []
    async for doc in db.predictions.aggregate(pipeline):
        date_str = f"{doc['_id']['year']}-{doc['_id']['month']:02d}-{doc['_id']['day']:02d}"
        result.append({"date": date_str, "count": doc["count"]})
    
    return result

# Admin routes
@app.post("/api/admin/doctors", response_model=DoctorResponse)
async def create_doctor(
    doctor: DoctorCreate,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    """Create new doctor (admin only)"""
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Check if doctor already exists
    existing_doctor = await db.doctors.find_one({"email": doctor.email})
    if existing_doctor:
        raise HTTPException(status_code=400, detail="Doctor already exists")
    
    doctor_dict = doctor.dict()
    doctor_dict["password_hash"] = get_password_hash(doctor.password)
    del doctor_dict["password"]
    doctor_dict["created_at"] = datetime.utcnow()
    
    result = await db.doctors.insert_one(doctor_dict)
    doctor_dict["id"] = str(result.inserted_id)
    
    return DoctorResponse(**doctor_dict)

@app.get("/api/admin/doctors", response_model=List[DoctorResponse])
async def get_doctors(
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    """Get all doctors (admin only)"""
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    cursor = db.doctors.find()
    doctors = []
    async for doctor in cursor:
        doctor["id"] = str(doctor["_id"])
        doctors.append(DoctorResponse(**doctor))
    return doctors

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)