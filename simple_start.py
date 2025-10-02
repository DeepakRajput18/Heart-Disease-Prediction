#!/usr/bin/env python3
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
            print("\n🛑 Server stopped")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("❌ ultra_simple.py not found")
        print("💡 Try running: python fix_commands.py")

if __name__ == "__main__":
    main()
