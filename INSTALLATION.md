# Heart Disease Prediction System - Installation Guide

## Quick Start (Recommended)

### Option 1: Ultra Simple Server (Minimal Dependencies)
```bash
# Install minimal requirements
pip install fastapi uvicorn

# Run the ultra simple server
python ultra_simple.py
```

### Option 2: Full System
```bash
# Install all dependencies
pip install -r requirements.txt

# Run the full system
python minimal_server.py
```

### Option 3: Automatic Setup
```bash
# Run the automatic setup script
python start.py
```

## System Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: At least 512MB RAM
- **Storage**: 100MB free space

## Dependencies

### Core Dependencies (Required)
- `fastapi` - Web framework
- `uvicorn` - ASGI server

### Full System Dependencies (Optional)
- `python-multipart` - Form data handling
- `python-jose[cryptography]` - JWT tokens
- `passlib[bcrypt]` - Password hashing
- `motor` - MongoDB async driver
- `python-dotenv` - Environment variables
- `aiofiles` - Async file operations

## Installation Steps

### Step 1: Check Python Version
```bash
python --version
# Should show Python 3.7 or higher
```

### Step 2: Install Dependencies
```bash
# Option A: Install minimal dependencies
pip install fastapi uvicorn

# Option B: Install all dependencies
pip install fastapi uvicorn python-multipart python-jose[cryptography] passlib[bcrypt] motor python-dotenv aiofiles

# Option C: Install from requirements file
pip install -r requirements.txt
```

### Step 3: Run the Server
```bash
# Option A: Ultra simple server (recommended for testing)
python ultra_simple.py

# Option B: Minimal server with more features
python minimal_server.py

# Option C: Full backend server (requires all dependencies)
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### Step 4: Access the Application
Open your web browser and go to:
- **Main Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Login Page**: http://localhost:8000/login

## Default Login Credentials

- **Admin**: admin@heartpredict.com / admin123
- **Doctor**: dr.smith@heartpredict.com / doctor123

## Troubleshooting

### Common Issues and Solutions

#### 1. "ModuleNotFoundError: No module named 'fastapi'"
**Solution**: Install FastAPI
```bash
pip install fastapi uvicorn
```

#### 2. "Port 8000 is already in use"
**Solution**: Use a different port
```bash
python ultra_simple.py --port 8001
# Or modify the port in the script
```

#### 3. "Permission denied" on Linux/macOS
**Solution**: Use sudo or virtual environment
```bash
# Option A: Use sudo (not recommended)
sudo pip install fastapi uvicorn

# Option B: Use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn
```

#### 4. Frontend files not loading
**Solution**: The system works without frontend files using built-in HTML pages

#### 5. Database connection errors
**Solution**: The system uses in-memory storage by default, no database required

### Advanced Troubleshooting

#### Check Python Installation
```bash
python --version
pip --version
which python  # On Windows: where python
```

#### Check Installed Packages
```bash
pip list | grep fastapi
pip list | grep uvicorn
```

#### Test FastAPI Installation
```bash
python -c "import fastapi; print('FastAPI version:', fastapi.__version__)"
python -c "import uvicorn; print('Uvicorn installed successfully')"
```

#### Manual Server Start
```bash
# Start with specific host and port
uvicorn ultra_simple:app --host 127.0.0.1 --port 8000

# Start with reload (for development)
uvicorn ultra_simple:app --reload

# Start with specific workers
uvicorn ultra_simple:app --workers 4
```

## Features Available

### Ultra Simple Server
- ✅ Basic web interface
- ✅ Health check endpoint
- ✅ Login functionality
- ✅ API documentation
- ✅ Mock authentication

### Minimal Server
- ✅ All ultra simple features
- ✅ Patient management
- ✅ Prediction system
- ✅ Dashboard statistics
- ✅ File serving (CSS/JS)

### Full Backend Server
- ✅ All minimal server features
- ✅ Database integration (MongoDB)
- ✅ JWT authentication
- ✅ Password hashing
- ✅ File uploads
- ✅ Advanced analytics

## Development Mode

For development with auto-reload:
```bash
uvicorn ultra_simple:app --reload --host 0.0.0.0 --port 8000
```

## Production Deployment

For production deployment:
```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn ultra_simple:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Docker Deployment (Optional)

If you have Docker installed:
```bash
# Build the image
docker build -t heart-disease-app .

# Run the container
docker run -p 8000:8000 heart-disease-app
```

## Support

If you encounter any issues:

1. Check this troubleshooting guide
2. Ensure Python 3.7+ is installed
3. Try the ultra simple server first
4. Check the console output for error messages
5. Verify all dependencies are installed correctly

## Success Indicators

You'll know the system is working when you see:
- ✅ "Server is Running Successfully!" message
- ✅ Ability to access http://localhost:8000
- ✅ API documentation at http://localhost:8000/docs
- ✅ Successful login with demo credentials

The system is designed to work with minimal setup and dependencies!