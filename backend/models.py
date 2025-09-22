from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    doctor = "doctor"

class GenderEnum(str, Enum):
    male = "male"
    female = "female"

class RiskLevelEnum(str, Enum):
    low = "Low Risk"
    high = "High Risk"

# Authentication Models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    doctor_info: 'DoctorInfo'

class DoctorInfo(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: RoleEnum
    specialization: str

# Doctor Models
class DoctorCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.doctor
    specialization: str
    phone: Optional[str] = None

class DoctorResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: RoleEnum
    specialization: str
    phone: Optional[str] = None
    created_at: datetime

# Patient Models
class PatientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    date_of_birth: datetime
    gender: GenderEnum
    address: str
    emergency_contact: str
    medical_history: Optional[str] = None

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    medical_history: Optional[str] = None

class PatientResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: str
    date_of_birth: datetime
    gender: GenderEnum
    address: str
    emergency_contact: str
    medical_history: Optional[str] = None
    created_at: datetime
    created_by: str

# Prediction Models
class PredictionCreate(BaseModel):
    patient_id: str
    age: int
    sex: int  # 1 = male, 0 = female
    cp: int  # chest pain type (0-3)
    trestbps: int  # resting blood pressure
    chol: int  # serum cholesterol
    fbs: int  # fasting blood sugar > 120 mg/dl (1 = true, 0 = false)
    restecg: int  # resting electrocardiographic results (0-2)
    thalach: int  # maximum heart rate achieved
    exang: int  # exercise induced angina (1 = yes, 0 = no)
    oldpeak: float  # ST depression induced by exercise
    slope: int  # slope of the peak exercise ST segment (0-2)
    ca: int  # number of major vessels colored by fluoroscopy (0-3)
    thal: int  # thalassemia (0-2)

class PredictionResponse(BaseModel):
    id: str
    patient_id: str
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int
    probability: float
    risk_level: RiskLevelEnum
    created_at: datetime
    created_by: str

# Dashboard Models
class DashboardStats(BaseModel):
    total_patients: int
    high_risk_patients: int
    recent_predictions: int
    total_predictions: int

# File Models
class FileResponse(BaseModel):
    id: str
    patient_id: str
    filename: str
    file_path: str
    content_type: str
    uploaded_at: datetime
    uploaded_by: str