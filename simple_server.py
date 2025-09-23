#!/usr/bin/env python3
"""
Simple server to run the Heart Disease Prediction System
This version has minimal dependencies and should work out of the box
"""

import sys
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    required_packages = ['fastapi', 'uvicorn']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installing missing packages...")
        
        import subprocess
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "fastapi", "uvicorn[standard]"
            ])
            print("✅ Packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please run:")
            print("   pip install fastapi uvicorn[standard]")
            return False
    
    return True

def main():
    """Start the server"""
    print("🫀 Heart Disease Prediction System")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required")
        print(f"   Current version: {sys.version}")
        return
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Check and install requirements
    if not check_requirements():
        return
    
    # Check if frontend files exist
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print("⚠️  Frontend directory not found")
        print("   The server will still work, but with basic HTML only")
    else:
        print("✅ Frontend files found")
    
    # Import and run the server
    try:
        import uvicorn
        from backend.main import app
        
        print("\n🚀 Starting server...")
        print("🌐 Open your browser and go to: http://localhost:8000")
        print("📧 Login with: admin@heartpredict.com / admin123")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Start the server
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8000, 
            reload=False,  # Disable reload for stability
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Please make sure all files are in the correct location")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        print("   Please check the error message above")

if __name__ == "__main__":
    main()