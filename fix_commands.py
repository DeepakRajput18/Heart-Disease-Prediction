#!/usr/bin/env python3
"""
Command fixer - automatically detects and fixes common command issues
"""

import subprocess
import sys
import os
from pathlib import Path
import platform

def detect_python_command():
    """Detect the correct Python command"""
    python_commands = ['python', 'python3', 'py']
    
    for cmd in python_commands:
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True)
            if result.returncode == 0 and 'Python 3' in result.stdout:
                print(f"✅ Found Python: {cmd}")
                return cmd
        except FileNotFoundError:
            continue
    
    print("❌ No suitable Python found")
    return None

def detect_pip_command():
    """Detect the correct pip command"""
    pip_commands = [
        ('python3 -m pip', ['python3', '-m', 'pip', '--version']),
        ('pip3', ['pip3', '--version']),
        ('pip', ['pip', '--version']),
        ('py -m pip', ['py', '-m', 'pip', '--version'])
    ]

    for cmd_name, cmd_list in pip_commands:
        try:
            result = subprocess.run(cmd_list, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"✅ Found pip: {cmd_name}")
                return cmd_name
        except FileNotFoundError:
            continue

    print("❌ No suitable pip found")
    return None

def fix_requirements():
    """Fix requirements installation"""
    print("🔧 Fixing requirements installation...")

    python_cmd = detect_python_command()
    pip_cmd = detect_pip_command()

    if not python_cmd:
        print("❌ Cannot fix requirements - Python not found")
        return False

    if not pip_cmd:
        print("🔧 Attempting to install pip...")
        try:
            subprocess.run([python_cmd, '-m', 'ensurepip', '--default-pip'], check=True)
            print("✅ pip installed successfully")
            pip_cmd = f"{python_cmd} -m pip"
        except subprocess.CalledProcessError:
            print("❌ Could not install pip")
            return False

    # Try minimal requirements first
    minimal_reqs = ["fastapi", "uvicorn[standard]"]

    for req in minimal_reqs:
        try:
            if 'py -m pip' in pip_cmd:
                subprocess.run(['py', '-m', 'pip', 'install', req], check=True)
            elif 'python' in pip_cmd:
                parts = pip_cmd.split()
                subprocess.run(parts + ['install', req], check=True)
            else:
                subprocess.run([pip_cmd, 'install', req], check=True)
            print(f"✅ Installed {req}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {req}")

    return True

def create_simple_start_script():
    """Create a simple start script that works everywhere"""
    script_content = '''#!/usr/bin/env python3
"""
Simple start script - works with minimal dependencies
"""

import sys
import subprocess
from pathlib import Path

def main():
    print("🫀 Heart Disease Prediction System")
    print("🚀 Starting simple server...")
    
    # Check if ultra_simple.py exists
    if Path("ultra_simple.py").exists():
        try:
            subprocess.run([sys.executable, "ultra_simple.py"])
        except KeyboardInterrupt:
            print("\\n🛑 Server stopped")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("❌ ultra_simple.py not found")
        print("💡 Try running: python fix_commands.py")

if __name__ == "__main__":
    main()
'''
    
    with open("simple_start.py", "w") as f:
        f.write(script_content)
    
    print("✅ Created simple_start.py")

def create_batch_files():
    """Create Windows batch files"""
    
    # start.bat
    start_bat = '''@echo off
echo 🫀 Heart Disease Prediction System
echo 🚀 Starting server...

REM Try different Python commands
py ultra_simple.py 2>nul
if %errorlevel% equ 0 goto :eof

python ultra_simple.py 2>nul
if %errorlevel% equ 0 goto :eof

python3 ultra_simple.py 2>nul
if %errorlevel% equ 0 goto :eof

echo ❌ Could not start server
echo 💡 Make sure Python is installed
pause
'''
    
    with open("start.bat", "w") as f:
        f.write(start_bat)
    
    # install.bat
    install_bat = '''@echo off
echo 📦 Installing dependencies...

REM Try different pip commands
py -m pip install fastapi uvicorn[standard] 2>nul
if %errorlevel% equ 0 goto success

pip install fastapi uvicorn[standard] 2>nul
if %errorlevel% equ 0 goto success

pip3 install fastapi uvicorn[standard] 2>nul
if %errorlevel% equ 0 goto success

echo ❌ Installation failed
pause
goto :eof

:success
echo ✅ Installation completed
pause
'''
    
    with open("install.bat", "w") as f:
        f.write(install_bat)
    
    print("✅ Created Windows batch files")

def create_shell_scripts():
    """Create Unix shell scripts"""
    
    # start.sh
    start_sh = '''#!/bin/bash
echo "🫀 Heart Disease Prediction System"
echo "🚀 Starting server..."

# Try different Python commands
if command -v python3 &> /dev/null; then
    python3 ultra_simple.py
elif command -v python &> /dev/null; then
    python ultra_simple.py
else
    echo "❌ Python not found"
    echo "💡 Please install Python 3.8+"
fi
'''
    
    with open("start.sh", "w") as f:
        f.write(start_sh)
    
    # Make executable
    try:
        os.chmod("start.sh", 0o755)
    except:
        pass
    
    # install.sh
    install_sh = '''#!/bin/bash
echo "📦 Installing dependencies..."

# Try different pip commands
if python3 -m pip install fastapi uvicorn[standard]; then
    echo "✅ Installation completed"
elif pip3 install fastapi uvicorn[standard]; then
    echo "✅ Installation completed"
elif pip install fastapi uvicorn[standard]; then
    echo "✅ Installation completed"
else
    echo "❌ Installation failed"
    echo "💡 Try: sudo apt-get install python3-pip"
fi
'''
    
    with open("install.sh", "w") as f:
        f.write(install_sh)
    
    # Make executable
    try:
        os.chmod("install.sh", 0o755)
    except:
        pass
    
    print("✅ Created Unix shell scripts")

def main():
    """Main fixer function"""
    print("🔧 Heart Disease Prediction System - Command Fixer")
    print("=" * 50)
    
    # Detect system
    system = platform.system()
    print(f"🖥️  Detected system: {system}")
    
    # Fix requirements
    fix_requirements()
    
    # Create simple start script
    create_simple_start_script()
    
    # Create platform-specific scripts
    if system == "Windows":
        create_batch_files()
    else:
        create_shell_scripts()
    
    print("\n✅ Command fixing completed!")
    print("\n🚀 You can now start the server with:")
    if system == "Windows":
        print("   start.bat")
        print("   OR")
    else:
        print("   ./start.sh")
        print("   OR")
    print("   python simple_start.py")
    print("   OR")
    print("   python ultra_simple.py")

if __name__ == "__main__":
    main()