@echo off
echo 🚀 Starting Sync Talk Kit Backend
echo.

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found. Please copy .env.example to .env and configure your settings.
    echo.
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

echo 📚 Installing dependencies...
pip install -r requirements.txt

echo 🔍 Checking database migrations...
dir /b db\migrations\

echo ⚡ Starting server...
echo    Backend will be available at: http://localhost:8000
echo    API docs: http://localhost:8000/docs
echo    Health check: http://localhost:8000/api/healthz
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
