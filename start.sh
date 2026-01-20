#!/bin/bash

# Voice Assistant Web App Startup Script

echo "🎙️ Starting Voice Assistant Web App..."
echo ""

# Check if we're in the right directory
if [ ! -d "backend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Navigate to backend
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    
    # Install Whisper
    echo "📥 Installing Whisper..."
    pip install git+https://github.com/openai/whisper.git
fi

# Create generated_audio directory if it doesn't exist
mkdir -p generated_audio

# Start the server
echo ""
echo "🚀 Starting server on http://localhost:8000"
echo "📱 Open your browser and navigate to: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python run.py

