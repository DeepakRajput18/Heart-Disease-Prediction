#!/usr/bin/env python3
"""
Complete startup script for Heart Disease Prediction System
This script will install dependencies and start the server
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description=""):
    """Run a command and handle errors"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ {description} - Failed")
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def main():
    print("🫀 Heart Disease Prediction System Setup")
    print("=" * 50)
    
    # Check Python version
    print(f"🐍 Python version: {sys.version}")
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required")
        return
    
    # Install pip if not available
    try:
        import pip
        print("✅ pip is available")
    except ImportError:
        print("❌ pip not found, please install pip first")
        return
    
    # Install required packages
    packages = [
        "fastapi",
        "uvicorn[standard]",
        "python-multipart",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "motor",
        "python-dotenv",
        "aiofiles"
    ]
    
    print("📦 Installing required packages...")
    for package in packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            print(f"⚠️ Failed to install {package}, continuing...")
    
    # Check if frontend files exist
    frontend_path = Path("frontend")
    if frontend_path.exists():
        print("✅ Frontend files found")
    else:
        print("⚠️ Frontend files not found, using minimal interface")
    
    # Create .env file if it doesn't exist
    env_path = Path(".env")
    if not env_path.exists():
        print("📝 Creating .env file...")
        with open(".env", "w") as f:
            f.write("""MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=heart_disease_db
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
""")
        print("✅ .env file created")
    
    # Try to start the server
    print("\n🚀 Starting server...")
    print("🌐 Open your browser and go to: http://localhost:8000")
    print("📧 Login with: admin@heartpredict.com / admin123")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Try different server options
    server_options = [
        ("python minimal_server.py", "Minimal server"),
        ("uvicorn backend.main:app --host 0.0.0.0 --port 8000", "Full backend server"),
        ("python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000", "Backend with python -m"),
        ("python run_server.py", "Run server script")
    ]
    
    for command, description in server_options:
        print(f"\n🔄 Trying: {description}")
        try:
            subprocess.run(command, shell=True, check=True)
            break
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed: {e}")
            continue
        except KeyboardInterrupt:
            print(f"\n🛑 Server stopped by user")
            break
        except Exception as e:
            print(f"❌ {description} error: {e}")
            continue
    
    print("\n✅ Setup complete!")

if __name__ == "__main__":
    main()