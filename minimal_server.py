#!/usr/bin/env python3
"""
Minimal server for Heart Disease Prediction System
This version removes complex dependencies and focuses on core functionality
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import os
from pathlib import Path
import json

# Simple in-memory storage
users_db = {
    "admin@heartpredict.com": {
        "id": "1",
        "name": "System Administrator",
        "email": "admin@heartpredict.com",
        "password": "admin123",
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
    description="Professional heart disease prediction system",
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

# Mount static files
try:
    frontend_path = Path("frontend")
    if frontend_path.exists():
        app.mount("/static", StaticFiles(directory="frontend"), name="static")
        print("✅ Static files mounted")
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
    except Exception as e:
        print(f"Error loading frontend: {e}")
    
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Heart Disease Prediction System</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .status { padding: 20px; background: #e8f5e8; border-radius: 8px; margin: 20px 0; }
            .login-form { background: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px 0; }
            input, button { padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 4px; }
            button { background: #007bff; color: white; cursor: pointer; }
            button:hover { background: #0056b3; }
            .hidden { display: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🫀 Heart Disease Prediction System</h1>
            
            <div id="loginSection">
                <div class="status">
                    <h2>✅ Server is Running!</h2>
                    <p>The backend server is working correctly.</p>
                </div>
                
                <div class="login-form">
                    <h3>Login</h3>
                    <form id="loginForm">
                        <div>
                            <input type="email" id="email" placeholder="Email" value="admin@heartpredict.com" required>
                        </div>
                        <div>
                            <input type="password" id="password" placeholder="Password" value="admin123" required>
                        </div>
                        <button type="submit">Login</button>
                    </form>
                </div>
            </div>
            
            <div id="dashboardSection" class="hidden">
                <h2>Dashboard</h2>
                <p>Welcome to the Heart Disease Prediction System!</p>
                <button onclick="logout()">Logout</button>
            </div>
            
            <div>
                <h3>API Endpoints:</h3>
                <ul>
                    <li><a href="/docs">📚 API Documentation</a></li>
                    <li><a href="/api/health">🏥 Health Check</a></li>
                </ul>
            </div>
        </div>
        
        <script>
            document.getElementById('loginForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                
                try {
                    const response = await fetch('/api/auth/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email, password })
                    });
                    
                    if (response.ok) {
                        document.getElementById('loginSection').classList.add('hidden');
                        document.getElementById('dashboardSection').classList.remove('hidden');
                    } else {
                        alert('Login failed');
                    }
                } catch (error) {
                    alert('Network error');
                }
            });
            
            function logout() {
                document.getElementById('loginSection').classList.remove('hidden');
                document.getElementById('dashboardSection').classList.add('hidden');
            }
        </script>
    </body>
    </html>
    """)

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
    
    # Simple risk calculation
    risk_score = 0
    if age > 60: risk_score += 0.3
    if chol > 240: risk_score += 0.3
    if trestbps > 140: risk_score += 0.2
    if prediction_data.get("sex") == 1: risk_score += 0.1
    if prediction_data.get("cp", 0) > 0: risk_score += 0.1
    
    probability = min(risk_score, 0.95)
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
        {"risk_level": "Low Risk", "count": max(low_risk, 15)},
        {"risk_level": "High Risk", "count": max(high_risk, 5)}
    ]

@app.get("/api/analytics/predictions-timeline")
async def get_predictions_timeline():
    """Get predictions timeline"""
    return [
        {"date": "2024-01-01", "count": 3},
        {"date": "2024-01-02", "count": 5},
        {"date": "2024-01-03", "count": 2},
        {"date": "2024-01-04", "count": 4},
        {"date": "2024-01-05", "count": 6}
    ]

# Serve CSS and JS files
@app.get("/css/{file_path:path}")
async def serve_css(file_path: str):
    """Serve CSS files"""
    file_location = Path(f"frontend/css/{file_path}")
    if file_location.exists():
        return FileResponse(file_location, media_type="text/css")
    raise HTTPException(status_code=404, detail="CSS file not found")

@app.get("/js/{file_path:path}")
async def serve_js(file_path: str):
    """Serve JavaScript files"""
    file_location = Path(f"frontend/js/{file_path}")
    if file_location.exists():
        return FileResponse(file_location, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="JavaScript file not found")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Heart Disease Prediction System...")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📧 Login credentials: admin@heartpredict.com / admin123")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)