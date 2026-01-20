#!/bin/bash

# Voice Assistant Backend Setup Script

echo "🎤 Voice Assistant Backend Setup"
echo "=================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Navigate to backend directory
cd "$(dirname "$0")/backend" || exit 1

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies (this may take a while)..."
echo "   Installing core dependencies first..."
pip install fastapi uvicorn[standard] python-multipart python-dotenv pydantic httpx

echo "   Installing Whisper (this may take a moment)..."
# Try installing whisper from git (works with Python 3.14)
pip install git+https://github.com/openai/whisper.git || {
    echo "   ⚠️  Git installation failed, trying alternative method..."
    pip install --upgrade setuptools wheel
    pip install openai-whisper || {
        echo "   ⚠️  Package installation failed, you may need to install manually"
    }
}

echo "   Installing ML dependencies..."
pip install transformers torch torchaudio numpy scipy pydub openai gtts

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# OpenAI API Key for GPT (optional, can use local models)
OPENAI_API_KEY=your_openai_api_key_here

# Model Configuration
WHISPER_MODEL=base
BERT_MODEL=bert-base-uncased
GPT_MODEL=gpt-3.5-turbo

# Server Configuration
HOST=0.0.0.0
PORT=8000
EOF
    echo "✅ .env file created. Please edit it to add your OpenAI API key (optional)."
else
    echo "✅ .env file already exists"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "To start the server:"
echo "  1. cd backend"
echo "  2. source venv/bin/activate"
echo "  3. python run.py"
echo ""
echo "The server will start on http://localhost:8000"
echo "Note: First run will download models, which may take several minutes."


