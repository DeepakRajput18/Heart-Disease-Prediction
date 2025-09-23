#!/usr/bin/env python3
"""
Development server runner for Heart Disease Prediction System
"""

import uvicorn
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Run the development server"""
    print("🚀 Starting Heart Disease Prediction System...")
    print("📁 Project root:", project_root)
    
    # Check if required directories exist
    frontend_dir = project_root / "frontend"
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return
    
    # Check if main files exist
    required_files = [
        "frontend/index.html",
        "frontend/css/styles.css",
        "frontend/js/app.js"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (project_root / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return
    
    print("✅ All required files found")
    print("🌐 Starting server on http://localhost:8000")
    print("📧 Default login: admin@heartpredict.com / admin123")
    print("🔄 Server will auto-reload on file changes")
    print("🛑 Press Ctrl+C to stop the server")
    
    # Run the server
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(project_root)],
        log_level="info"
    )

if __name__ == "__main__":
    main()