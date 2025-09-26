#!/usr/bin/env python3
"""
Universal command runner for Heart Disease Prediction System
This script handles all common commands and provides fallbacks
"""

import subprocess
import sys
import os
from pathlib import Path
import argparse

def run_command(command, description="", shell=True):
    """Run a command with error handling"""
    print(f"🔄 {description}")
    try:
        if shell:
            result = subprocess.run(command, shell=True, check=True, text=True)
        else:
            result = subprocess.run(command, check=True, text=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed: {e}")
        return False
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def check_python():
    """Check Python version and availability"""
    try:
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
            return False
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    except Exception as e:
        print(f"❌ Python check failed: {e}")
        return False

def install_requirements():
    """Install Python requirements with fallbacks"""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    # Try different pip commands
    pip_commands = [
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        ["pip3", "install", "-r", "requirements.txt"],
        ["pip", "install", "-r", "requirements.txt"]
    ]
    
    for cmd in pip_commands:
        try:
            print(f"🔄 Trying: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print("✅ Requirements installed successfully")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    print("❌ Failed to install requirements with all methods")
    return False

def start_server(server_type="auto"):
    """Start the server with different options"""
    
    if not check_python():
        return False
    
    # Check if requirements are installed
    try:
        import fastapi
        import uvicorn
        print("✅ Dependencies available")
    except ImportError:
        print("📦 Installing dependencies...")
        if not install_requirements():
            print("❌ Failed to install dependencies")
            return False
    
    # Server options in order of preference
    server_options = []
    
    if server_type == "simple" or server_type == "auto":
        server_options.append(
            ([sys.executable, "ultra_simple.py"], "Ultra Simple Server")
        )
    
    if server_type == "minimal" or server_type == "auto":
        server_options.append(
            ([sys.executable, "minimal_server.py"], "Minimal Server")
        )
    
    if server_type == "full" or server_type == "auto":
        server_options.extend([
            ([sys.executable, "run_server.py"], "Development Server"),
            ([sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"], "Uvicorn Server"),
            (["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"], "Direct Uvicorn")
        ])
    
    for cmd, description in server_options:
        print(f"\n🚀 Trying: {description}")
        try:
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed: {e}")
            continue
        except FileNotFoundError as e:
            print(f"❌ {description} - Command not found: {e}")
            continue
        except KeyboardInterrupt:
            print(f"\n🛑 Server stopped by user")
            return True
        except Exception as e:
            print(f"❌ {description} error: {e}")
            continue
    
    print("❌ All server options failed")
    return False

def run_tests():
    """Run tests with fallbacks"""
    test_commands = [
        [sys.executable, "-m", "pytest", "tests/", "-v"],
        ["pytest", "tests/", "-v"],
        [sys.executable, "-m", "pytest", "-v"],
        ["python", "-m", "unittest", "discover", "tests"]
    ]
    
    for cmd in test_commands:
        try:
            print(f"🔄 Trying: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print("✅ Tests completed successfully")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    print("❌ All test commands failed")
    return False

def init_database():
    """Initialize database"""
    init_commands = [
        [sys.executable, "init_db.py"],
        ["python3", "init_db.py"],
        ["python", "init_db.py"]
    ]
    
    for cmd in init_commands:
        try:
            print(f"🔄 Trying: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print("✅ Database initialized successfully")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    print("❌ Database initialization failed")
    return False

def docker_operations(operation):
    """Handle Docker operations"""
    docker_commands = {
        "build": ["docker", "build", "-t", "heart-disease-app", "."],
        "run": ["docker", "run", "-p", "8000:8000", "heart-disease-app"],
        "compose-up": ["docker-compose", "up", "-d"],
        "compose-down": ["docker-compose", "down"]
    }
    
    if operation not in docker_commands:
        print(f"❌ Unknown Docker operation: {operation}")
        return False
    
    cmd = docker_commands[operation]
    try:
        print(f"🔄 Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        print(f"✅ Docker {operation} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker {operation} failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ Docker not found. Please install Docker first.")
        return False

def main():
    """Main command handler"""
    parser = argparse.ArgumentParser(description="Heart Disease Prediction System Command Runner")
    parser.add_argument("command", choices=[
        "install", "start", "dev", "simple", "minimal", "full",
        "test", "init-db", "docker-build", "docker-run", 
        "docker-compose-up", "docker-compose-down", "setup"
    ], help="Command to run")
    
    args = parser.parse_args()
    
    print("🫀 Heart Disease Prediction System")
    print("=" * 50)
    
    if args.command == "install":
        install_requirements()
    elif args.command == "setup":
        print("🔧 Setting up the system...")
        install_requirements()
        init_database()
    elif args.command in ["start", "dev"]:
        start_server("auto")
    elif args.command == "simple":
        start_server("simple")
    elif args.command == "minimal":
        start_server("minimal")
    elif args.command == "full":
        start_server("full")
    elif args.command == "test":
        run_tests()
    elif args.command == "init-db":
        init_database()
    elif args.command.startswith("docker"):
        operation = args.command.replace("docker-", "")
        docker_operations(operation)
    else:
        print(f"❌ Unknown command: {args.command}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("🫀 Heart Disease Prediction System - Command Runner")
        print("\nAvailable commands:")
        print("  python run_commands.py install     - Install dependencies")
        print("  python run_commands.py setup       - Full setup (install + init-db)")
        print("  python run_commands.py start       - Start server (auto-detect)")
        print("  python run_commands.py simple      - Start ultra simple server")
        print("  python run_commands.py minimal     - Start minimal server")
        print("  python run_commands.py full        - Start full server")
        print("  python run_commands.py test        - Run tests")
        print("  python run_commands.py init-db     - Initialize database")
        print("  python run_commands.py docker-build - Build Docker image")
        print("  python run_commands.py docker-run  - Run Docker container")
        print("\nExample: python run_commands.py start")
    else:
        main()