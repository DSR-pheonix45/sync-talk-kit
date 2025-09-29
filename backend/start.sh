#!/bin/bash
# Backend startup script

echo "🚀 Starting Sync Talk Kit Backend"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Please copy .env.example to .env and configure your settings."
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📚 Installing dependencies..."
pip install -r requirements.txt

echo "🔍 Checking database migrations..."
# List migration files
ls -la db/migrations/

echo "⚡ Starting server..."
echo "   Backend will be available at: http://localhost:8000"
echo "   API docs: http://localhost:8000/docs"
echo "   Health check: http://localhost:8000/api/healthz"

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
