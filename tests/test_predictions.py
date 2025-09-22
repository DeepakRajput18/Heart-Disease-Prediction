import pytest
from httpx import AsyncClient
from backend.main import app

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def auth_headers(client):
    """Get authentication headers"""
    response = await client.post("/api/auth/login", json={
        "email": "admin@heartpredict.com",
        "password": "admin123"
    })
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    else:
        pytest.skip("Authentication failed - admin user not available")

@pytest.fixture
async def sample_patient(client, auth_headers):
    """Create a sample patient for testing"""
    patient_data = {
        "name": "Test Patient for Prediction",
        "email": "prediction.test@email.com",
        "phone": "+1-555-0125",
        "date_of_birth": "1980-01-01T00:00:00",
        "gender": "male",
        "address": "123 Prediction St",
        "emergency_contact": "Emergency Contact",
        "medical_history": "Test patient for predictions"
    }
    
    response = await client.post("/api/patients", json=patient_data, headers=auth_headers)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        pytest.skip("Could not create sample patient")

@pytest.mark.anyio
async def test_create_prediction(client, auth_headers, sample_patient):
    """Test creating a heart disease prediction"""
    prediction_data = {
        "patient_id": sample_patient,
        "age": 54,
        "sex": 1,
        "cp": 0,
        "trestbps": 140,
        "chol": 239,
        "fbs": 0,
        "restecg": 1,
        "thalach": 160,
        "exang": 0,
        "oldpeak": 1.2,
        "slope": 2,
        "ca": 0,
        "thal": 2
    }
    
    response = await client.post("/api/predictions", json=prediction_data, headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "probability" in data
    assert "risk_level" in data
    assert data["risk_level"] in ["Low Risk", "High Risk"]
    assert 0 <= data["probability"] <= 1
    assert data["patient_id"] == sample_patient

@pytest.mark.anyio
async def test_create_prediction_invalid_patient(client, auth_headers):
    """Test creating prediction with invalid patient ID"""
    prediction_data = {
        "patient_id": "invalid_patient_id",
        "age": 54,
        "sex": 1,
        "cp": 0,
        "trestbps": 140,
        "chol": 239,
        "fbs": 0,
        "restecg": 1,
        "thalach": 160,
        "exang": 0,
        "oldpeak": 1.2,
        "slope": 2,
        "ca": 0,
        "thal": 2
    }
    
    response = await client.post("/api/predictions", json=prediction_data, headers=auth_headers)
    
    # This might return 400 or 422 depending on validation
    assert response.status_code in [400, 422]

@pytest.mark.anyio
async def test_create_prediction_invalid_values(client, auth_headers, sample_patient):
    """Test creating prediction with invalid clinical values"""
    prediction_data = {
        "patient_id": sample_patient,
        "age": -5,  # Invalid age
        "sex": 1,
        "cp": 0,
        "trestbps": 140,
        "chol": 239,
        "fbs": 0,
        "restecg": 1,
        "thalach": 160,
        "exang": 0,
        "oldpeak": 1.2,
        "slope": 2,
        "ca": 0,
        "thal": 2
    }
    
    response = await client.post("/api/predictions", json=prediction_data, headers=auth_headers)
    
    assert response.status_code == 422  # Validation error

@pytest.mark.anyio
async def test_get_patient_predictions(client, auth_headers, sample_patient):
    """Test getting predictions for a patient"""
    # First create a prediction
    prediction_data = {
        "patient_id": sample_patient,
        "age": 54,
        "sex": 1,
        "cp": 0,
        "trestbps": 140,
        "chol": 239,
        "fbs": 0,
        "restecg": 1,
        "thalach": 160,
        "exang": 0,
        "oldpeak": 1.2,
        "slope": 2,
        "ca": 0,
        "thal": 2
    }
    
    await client.post("/api/predictions", json=prediction_data, headers=auth_headers)
    
    # Now get predictions for the patient
    response = await client.get(f"/api/predictions/{sample_patient}", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "probability" in data[0]
        assert "risk_level" in data[0]

@pytest.mark.anyio
async def test_prediction_model_consistency(client, auth_headers, sample_patient):
    """Test that the same input produces consistent results"""
    prediction_data = {
        "patient_id": sample_patient,
        "age": 54,
        "sex": 1,
        "cp": 0,
        "trestbps": 140,
        "chol": 239,
        "fbs": 0,
        "restecg": 1,
        "thalach": 160,
        "exang": 0,
        "oldpeak": 1.2,
        "slope": 2,
        "ca": 0,
        "thal": 2
    }
    
    # Make two identical predictions
    response1 = await client.post("/api/predictions", json=prediction_data, headers=auth_headers)
    response2 = await client.post("/api/predictions", json=prediction_data, headers=auth_headers)
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    data1 = response1.json()
    data2 = response2.json()
    
    # Results should be identical (same model, same input)
    assert data1["probability"] == data2["probability"]
    assert data1["risk_level"] == data2["risk_level"]