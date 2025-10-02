#!/bin/bash
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
