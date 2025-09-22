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

@pytest.mark.anyio
async def test_create_patient(client, auth_headers):
    """Test creating a new patient"""
    patient_data = {
        "name": "Test Patient",
        "email": "test.patient@email.com",
        "phone": "+1-555-0123",
        "date_of_birth": "1990-01-01T00:00:00",
        "gender": "male",
        "address": "123 Test St, Test City, TS 12345",
        "emergency_contact": "Emergency Contact - +1-555-0124",
        "medical_history": "No significant medical history"
    }
    
    response = await client.post("/api/patients", json=patient_data, headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == patient_data["name"]
    assert data["email"] == patient_data["email"]
    assert "id" in data

@pytest.mark.anyio
async def test_get_patients(client, auth_headers):
    """Test getting list of patients"""
    response = await client.get("/api/patients", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.anyio
async def test_create_patient_invalid_email(client, auth_headers):
    """Test creating patient with invalid email"""
    patient_data = {
        "name": "Test Patient",
        "email": "invalid-email",
        "phone": "+1-555-0123",
        "date_of_birth": "1990-01-01T00:00:00",
        "gender": "male",
        "address": "123 Test St",
        "emergency_contact": "Emergency Contact"
    }
    
    response = await client.post("/api/patients", json=patient_data, headers=auth_headers)
    
    assert response.status_code == 422  # Validation error

@pytest.mark.anyio
async def test_create_patient_missing_fields(client, auth_headers):
    """Test creating patient with missing required fields"""
    patient_data = {
        "name": "Test Patient",
        # Missing required fields
    }
    
    response = await client.post("/api/patients", json=patient_data, headers=auth_headers)
    
    assert response.status_code == 422  # Validation error

@pytest.mark.anyio
async def test_get_patient_not_found(client, auth_headers):
    """Test getting non-existent patient"""
    fake_id = "507f1f77bcf86cd799439011"  # Valid ObjectId format
    response = await client.get(f"/api/patients/{fake_id}", headers=auth_headers)
    
    assert response.status_code == 404

@pytest.mark.anyio
async def test_delete_patient_not_found(client, auth_headers):
    """Test deleting non-existent patient"""
    fake_id = "507f1f77bcf86cd799439011"  # Valid ObjectId format
    response = await client.delete(f"/api/patients/{fake_id}", headers=auth_headers)
    
    assert response.status_code == 404