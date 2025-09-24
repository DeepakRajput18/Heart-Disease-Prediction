#!/usr/bin/env python3
"""
Quick development server starter
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Start the development server with proper setup"""
    print("🔧 Setting up Heart Disease Prediction System...")
    
    # Change to project directory
    project_root = Path(__file__).parent
    import os
    try:
        os.chdir(project_root)
    except AttributeError as e:
        print(f"❌ OS module error: {e}")
        print("💡 Try running: python -c 'import os; print(os.__file__)'")
        return
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return
    
    print("✅ Python version OK")
    
    # Install requirements if needed
    try:
        import fastapi
        import uvicorn
        print("✅ Dependencies already installed")
    except ImportError:
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Start the server
    print("🚀 Starting development server...")
    print("🌐 Open http://localhost:8000 in your browser")
    print("📧 Login: admin@heartpredict.com / admin123")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "backend.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")

if __name__ == "__main__":
    main()