from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from datetime import datetime, timedelta
import uvicorn
import os
from pathlib import Path
from typing import List, Optional
import json

# Simple in-memory storage for development
users_db = {
    "admin@heartpredict.com": {
        "id": "1",
        "name": "System Administrator",
        "email": "admin@heartpredict.com",
        "password": "admin123",  # In production, this would be hashed
        "role": "admin",
        "specialization": "System Administration"
    },
    "dr.smith@heartpredict.com": {
        "id": "2", 
        "name": "Dr. John Smith",
        "email": "dr.smith@heartpredict.com",
        "password": "doctor123",
        "role": "doctor",
        "specialization": "Cardiology"
    }
}

patients_db = []
predictions_db = []

app = FastAPI(
    title="Heart Disease Prediction API",
    description="Professional heart disease prediction system for medical professionals",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files - try different approaches
try:
    # Check if frontend directory exists
    frontend_path = Path("frontend")
    if frontend_path.exists():
        app.mount("/static", StaticFiles(directory="frontend"), name="static")
        print("✅ Static files mounted from frontend/")
    else:
        print("⚠️ Frontend directory not found")
except Exception as e:
    print(f"⚠️ Could not mount static files: {e}")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    try:
        html_path = Path("frontend/index.html")
        if html_path.exists():
            with open(html_path, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        else:
            # Return a simple HTML page if frontend files don't exist
            return HTMLResponse(content="""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Heart Disease Prediction System</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .container { max-width: 600px; margin: 0 auto; text-align: center; }
                    .status { padding: 20px; background: #e8f5e8; border-radius: 8px; margin: 20px 0; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🫀 Heart Disease Prediction System</h1>
                    <div class="status">
                        <h2>✅ Server is Running!</h2>
                        <p>The backend server is working correctly.</p>
                        <p>Frontend files are being loaded...</p>
                    </div>
                    <div>
                        <h3>API Endpoints:</h3>
                        <ul style="text-align: left;">
                            <li><a href="/docs">📚 API Documentation</a></li>
                            <li><a href="/api/health">🏥 Health Check</a></li>
                        </ul>
                    </div>
                </div>
            </body>
            </html>
            """)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Server Running</h1><p>Error loading frontend: {e}</p>")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Heart Disease Prediction API is running",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/auth/login")
async def login(credentials: dict):
    """Simple login endpoint"""
    email = credentials.get("email")
    password = credentials.get("password")
    
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")
    
    user = users_db.get(email)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Return user info (in production, return JWT token)
    return {
        "access_token": "mock_token_" + user["id"],
        "token_type": "bearer",
        "doctor_info": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "specialization": user["specialization"]
        }
    }

@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    return {
        "total_patients": len(patients_db),
        "high_risk_patients": len([p for p in predictions_db if p.get("risk_level") == "High Risk"]),
        "recent_predictions": len([p for p in predictions_db if (datetime.utcnow() - datetime.fromisoformat(p.get("created_at", "2024-01-01T00:00:00"))).days <= 7]),
        "total_predictions": len(predictions_db)
    }

@app.post("/api/patients")
async def create_patient(patient: dict):
    """Create a new patient"""
    patient["id"] = str(len(patients_db) + 1)
    patient["created_at"] = datetime.utcnow().isoformat()
    patients_db.append(patient)
    return patient

@app.get("/api/patients")
async def get_patients():
    """Get all patients"""
    return patients_db

@app.post("/api/predictions")
async def create_prediction(prediction_data: dict):
    """Create heart disease prediction"""
    # Simple mock prediction logic
    age = prediction_data.get("age", 50)
    chol = prediction_data.get("chol", 200)
    trestbps = prediction_data.get("trestbps", 120)
    
    # Simple risk calculation based on age, cholesterol, and blood pressure
    risk_score = 0
    if age > 60: risk_score += 0.3
    if chol > 240: risk_score += 0.3
    if trestbps > 140: risk_score += 0.2
    if prediction_data.get("sex") == 1: risk_score += 0.1  # Male
    if prediction_data.get("cp", 0) > 0: risk_score += 0.1  # Chest pain
    
    probability = min(risk_score, 0.95)  # Cap at 95%
    risk_level = "High Risk" if probability >= 0.5 else "Low Risk"
    
    prediction = {
        **prediction_data,
        "id": str(len(predictions_db) + 1),
        "probability": probability,
        "risk_level": risk_level,
        "created_at": datetime.utcnow().isoformat()
    }
    
    predictions_db.append(prediction)
    return prediction

@app.get("/api/predictions/{patient_id}")
async def get_patient_predictions(patient_id: str):
    """Get predictions for a patient"""
    return [p for p in predictions_db if p.get("patient_id") == patient_id]

@app.get("/api/analytics/risk-distribution")
async def get_risk_distribution():
    """Get risk distribution analytics"""
    high_risk = len([p for p in predictions_db if p.get("risk_level") == "High Risk"])
    low_risk = len([p for p in predictions_db if p.get("risk_level") == "Low Risk"])
    
    return [
        {"risk_level": "Low Risk", "count": max(low_risk, 15)},  # Mock data if empty
        {"risk_level": "High Risk", "count": max(high_risk, 5)}
    ]

@app.get("/api/analytics/predictions-timeline")
async def get_predictions_timeline():
    """Get predictions timeline"""
    # Mock timeline data
    return [
        {"date": "2024-01-01", "count": 3},
        {"date": "2024-01-02", "count": 5},
        {"date": "2024-01-03", "count": 2},
        {"date": "2024-01-04", "count": 4},
        {"date": "2024-01-05", "count": 6}
    ]

# Serve CSS files
@app.get("/css/{file_path:path}")
async def serve_css(file_path: str):
    """Serve CSS files"""
    file_location = Path(f"frontend/css/{file_path}")
    if file_location.exists():
        return FileResponse(file_location, media_type="text/css")
    raise HTTPException(status_code=404, detail="CSS file not found")

# Serve JS files  
@app.get("/js/{file_path:path}")
async def serve_js(file_path: str):
    """Serve JavaScript files"""
    file_location = Path(f"frontend/js/{file_path}")
    if file_location.exists():
        return FileResponse(file_location, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="JavaScript file not found")

if __name__ == "__main__":
    print("🚀 Starting Heart Disease Prediction System...")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📧 Login credentials: admin@heartpredict.com / admin123")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)