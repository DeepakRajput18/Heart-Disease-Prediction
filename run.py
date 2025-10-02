#!/usr/bin/env python3
"""
Universal run script for Heart Disease Prediction System
Handles all npm scripts and make commands with proper error handling
"""

import subprocess
import sys
import os
from pathlib import Path
import argparse

def ensure_pip():
    """Ensure pip is available"""
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'],
                                capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ pip is available")
            return True
    except:
        pass

    print("🔧 Installing pip...")
    try:
        subprocess.run([sys.executable, '-m', 'ensurepip', '--default-pip'],
                       check=True, capture_output=True)
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'],
                       capture_output=True)
        print("✅ pip installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install pip")
        return False

def install_requirements(minimal=False):
    """Install requirements"""
    if not ensure_pip():
        return False

    print("📦 Installing dependencies...")

    if minimal:
        packages = ["fastapi", "uvicorn[standard]"]
        for pkg in packages:
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', pkg],
                               check=True, capture_output=True)
                print(f"✅ Installed {pkg}")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {pkg}")
    else:
        req_file = Path("requirements.txt")
        if not req_file.exists():
            print("❌ requirements.txt not found")
            return False

        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                           check=True)
            print("✅ Dependencies installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False

    return True

def start_server(server_type="minimal"):
    """Start the server"""
    servers = {
        "simple": "ultra_simple.py",
        "minimal": "minimal_server.py",
        "dev": "run_server.py",
        "full": "start_server.py"
    }

    script = servers.get(server_type, "minimal_server.py")

    if not Path(script).exists():
        print(f"❌ {script} not found")
        return False

    print(f"🚀 Starting {server_type} server...")
    print("🌐 Server will be available at http://localhost:8000")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)

    try:
        subprocess.run([sys.executable, script])
        return True
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_tests():
    """Run tests"""
    print("🧪 Running tests...")

    # Check if pytest is installed
    try:
        subprocess.run([sys.executable, '-m', 'pytest', '--version'],
                       capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("📦 Installing pytest...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pytest'],
                           check=True, capture_output=True)
        except:
            print("❌ Failed to install pytest")
            return False

    try:
        subprocess.run([sys.executable, '-m', 'pytest', 'tests/', '-v'], check=True)
        print("✅ Tests passed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Tests failed")
        return False

def init_database():
    """Initialize database"""
    print("🗄️ Initializing database...")

    if not Path("init_db.py").exists():
        print("❌ init_db.py not found")
        return False

    try:
        subprocess.run([sys.executable, 'init_db.py'], check=True)
        print("✅ Database initialized")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def docker_command(cmd):
    """Run docker commands"""
    docker_cmds = {
        "build": ["docker", "build", "-t", "heart-disease-app", "."],
        "run": ["docker", "run", "-p", "8000:8000", "heart-disease-app"],
        "compose-up": ["docker-compose", "up", "-d"],
        "compose-down": ["docker-compose", "down"]
    }

    if cmd not in docker_cmds:
        print(f"❌ Unknown docker command: {cmd}")
        return False

    print(f"🐳 Running docker {cmd}...")
    try:
        subprocess.run(docker_cmds[cmd], check=True)
        print(f"✅ Docker {cmd} completed")
        return True
    except FileNotFoundError:
        print("❌ Docker not found. Please install Docker first.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker command failed: {e}")
        return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Heart Disease Prediction System - Universal Runner"
    )
    parser.add_argument(
        'command',
        choices=[
            'install', 'install-minimal', 'setup', 'fix',
            'start', 'dev', 'simple', 'minimal', 'full',
            'test', 'init-db',
            'docker-build', 'docker-run', 'docker-compose-up', 'docker-compose-down'
        ],
        help='Command to run'
    )

    args = parser.parse_args()

    print("🫀 Heart Disease Prediction System")
    print("=" * 50)

    # Handle commands
    if args.command == 'install':
        success = install_requirements(minimal=False)
    elif args.command == 'install-minimal':
        success = install_requirements(minimal=True)
    elif args.command == 'setup':
        success = install_requirements() and init_database()
    elif args.command == 'fix':
        subprocess.run([sys.executable, 'fix_commands.py'])
        success = True
    elif args.command in ['start', 'minimal']:
        success = start_server('minimal')
    elif args.command == 'dev':
        success = start_server('dev')
    elif args.command == 'simple':
        success = start_server('simple')
    elif args.command == 'full':
        success = start_server('full')
    elif args.command == 'test':
        success = run_tests()
    elif args.command == 'init-db':
        success = init_database()
    elif args.command.startswith('docker'):
        docker_cmd = args.command.replace('docker-', '').replace('-', '-')
        success = docker_command(docker_cmd)
    else:
        print(f"❌ Unknown command: {args.command}")
        success = False

    return 0 if success else 1

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("🫀 Heart Disease Prediction System - Universal Runner")
        print("\nUsage: python3 run.py <command>")
        print("\nAvailable commands:")
        print("  install           - Install all dependencies")
        print("  install-minimal   - Install minimal dependencies (fastapi, uvicorn)")
        print("  setup             - Full setup (install + database)")
        print("  fix               - Fix common issues")
        print("  start/minimal     - Start minimal server")
        print("  dev               - Start development server")
        print("  simple            - Start ultra simple server")
        print("  full              - Start full server")
        print("  test              - Run tests")
        print("  init-db           - Initialize database")
        print("  docker-build      - Build Docker image")
        print("  docker-run        - Run Docker container")
        print("  docker-compose-up - Start with Docker Compose")
        print("\nExamples:")
        print("  python3 run.py install")
        print("  python3 run.py start")
        print("  python3 run.py test")
        sys.exit(0)

    sys.exit(main())
