#!/bin/bash
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
