#!/bin/bash
# Ecommerce Flask Server Startup Script
# This script activates the virtual environment and starts the Flask server

echo "🚀 Starting Ecommerce Flask Application"
echo "========================================"

# Navigate to project directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip install -q flask flask-cors

# Start the Flask application
echo "🔥 Starting Flask server..."
python3 run.py
