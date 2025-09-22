import pytest
import asyncio
from httpx import AsyncClient
from backend.main import app

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.anyio
async def test_login_success(client):
    """Test successful login"""
    # This test assumes the admin user exists
    response = await client.post("/api/auth/login", json={
        "email": "admin@heartpredict.com",
        "password": "admin123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "doctor_info" in data

@pytest.mark.anyio
async def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = await client.post("/api/auth/login", json={
        "email": "invalid@email.com",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data

@pytest.mark.anyio
async def test_login_missing_fields(client):
    """Test login with missing fields"""
    response = await client.post("/api/auth/login", json={
        "email": "test@email.com"
        # Missing password
    })
    
    assert response.status_code == 422  # Validation error

@pytest.mark.anyio
async def test_protected_route_without_token(client):
    """Test accessing protected route without token"""
    response = await client.get("/api/dashboard/stats")
    
    assert response.status_code == 401

@pytest.mark.anyio
async def test_protected_route_with_invalid_token(client):
    """Test accessing protected route with invalid token"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = await client.get("/api/dashboard/stats", headers=headers)
    
    assert response.status_code == 401