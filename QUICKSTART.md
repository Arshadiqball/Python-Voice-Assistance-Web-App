# Quick Start Guide

Get your Voice Assistant Web App running in 5 minutes!

## Step 1: Setup Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install git+https://github.com/openai/whisper.git
```

## Step 2: Start Backend Server

```bash
python run.py
```

The backend will run on **port 8000**.

## Step 3: Start Web Frontend (New Terminal)

From the project root directory:

```bash
python web_server.py
```

The web frontend will run on **port 3000**.

## Step 4: Open Browser

Navigate to: **http://localhost:3000**

## Step 4: Use the App

1. **Click the microphone** to record voice
2. **Or type** your message in the text field
3. **Get AI responses** with audio playback

## Optional: Add OpenAI API Key

For better GPT responses, create `backend/.env`:

```env
OPENAI_API_KEY=your_key_here
```

That's it! 🎉
