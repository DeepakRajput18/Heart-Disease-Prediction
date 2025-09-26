#!/usr/bin/env python3
"""
Universal server starter - tries multiple methods to start the server
"""

import subprocess
import sys
import os
from pathlib import Path
import argparse
import time

def check_port(port=8000):
    """Check if port is available"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def find_available_port(start_port=8000):
    """Find an available port"""
    for port in range(start_port, start_port + 100):
        if check_port(port):
            return port
    return None

def install_minimal_deps():
    """Install minimal dependencies"""
    print("📦 Installing minimal dependencies...")
    
    commands = [
        [sys.executable, "-m", "pip", "install", "fastapi", "uvicorn[standard]"],
        ["pip3", "install", "fastapi", "uvicorn[standard]"],
        ["pip", "install", "fastapi", "uvicorn[standard]"]
    ]
    
    for cmd in commands:
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print("✅ Dependencies installed")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    print("❌ Failed to install dependencies")
    return False

def start_server(port=8000, auto_port=True):
    """Start server with multiple fallback options"""
    
    # Check if port is available
    if not check_port(port) and auto_port:
        new_port = find_available_port(port)
        if new_port:
            print(f"⚠️ Port {port} is busy, using port {new_port}")
            port = new_port
        else:
            print(f"❌ No available ports found")
            return False
    
    # Server startup options
    server_options = [
        # Ultra simple server
        {
            "cmd": [sys.executable, "ultra_simple.py"],
            "name": "Ultra Simple Server",
            "modify_port": False
        },
        # Minimal server
        {
            "cmd": [sys.executable, "minimal_server.py"],
            "name": "Minimal Server",
            "modify_port": False
        },
        # Direct uvicorn
        {
            "cmd": [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", str(port)],
            "name": "Uvicorn Backend",
            "modify_port": True
        },
        # System uvicorn
        {
            "cmd": ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", str(port)],
            "name": "System Uvicorn",
            "modify_port": True
        }
    ]
    
    for option in server_options:
        print(f"\n🚀 Trying: {option['name']}")
        
        # Check if the script file exists for file-based servers
        if option["cmd"][1].endswith('.py'):
            if not Path(option["cmd"][1]).exists():
                print(f"❌ {option['cmd'][1]} not found")
                continue
        
        try:
            # Modify port if needed
            cmd = option["cmd"].copy()
            if option["modify_port"] and port != 8000:
                # Replace port in command
                for i, arg in enumerate(cmd):
                    if arg == "8000":
                        cmd[i] = str(port)
            
            print(f"   Command: {' '.join(cmd)}")
            
            # Start the server
            process = subprocess.Popen(cmd)
            
            # Wait a bit to see if it starts successfully
            time.sleep(2)
            
            if process.poll() is None:  # Process is still running
                print(f"✅ {option['name']} started successfully!")
                print(f"🌐 Open your browser: http://localhost:{port}")
                
                try:
                    process.wait()  # Wait for the process to finish
                except KeyboardInterrupt:
                    print(f"\n🛑 Stopping {option['name']}...")
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                    print("✅ Server stopped")
                
                return True
            else:
                print(f"❌ {option['name']} failed to start")
                
        except FileNotFoundError:
            print(f"❌ Command not found: {option['cmd'][0]}")
        except Exception as e:
            print(f"❌ Error starting {option['name']}: {e}")
    
    print("\n❌ All server options failed")
    return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Universal Server Starter")
    parser.add_argument("--port", type=int, default=8000, help="Port to run server on")
    parser.add_argument("--no-auto-port", action="store_true", help="Don't automatically find available port")
    parser.add_argument("--install", action="store_true", help="Install dependencies first")
    
    args = parser.parse_args()
    
    print("🫀 Heart Disease Prediction System - Universal Starter")
    print("=" * 55)
    
    # Install dependencies if requested
    if args.install:
        if not install_minimal_deps():
            print("❌ Failed to install dependencies")
            return
    
    # Check Python version
    if sys.version_info < (3, 7):
        print(f"❌ Python 3.7+ required, found {sys.version_info.major}.{sys.version_info.minor}")
        return
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Start server
    success = start_server(args.port, not args.no_auto_port)
    
    if not success:
        print("\n💡 Troubleshooting tips:")
        print("1. Install dependencies: python start_server.py --install")
        print("2. Try a different port: python start_server.py --port 8001")
        print("3. Check if Python and pip are installed correctly")
        print("4. Run: python fix_commands.py")

if __name__ == "__main__":
    main()