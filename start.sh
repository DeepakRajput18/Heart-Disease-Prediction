#!/bin/bash
echo "🫀 Heart Disease Prediction System"
echo "🚀 Starting server..."

# Try different Python commands
if command -v python3 &> /dev/null; then
    python3 standalone_server.py
elif command -v python &> /dev/null; then
    python standalone_server.py
else
    echo "❌ Python not found"
    echo "💡 Please install Python 3.8+"
fi
