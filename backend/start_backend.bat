@echo off
echo 🚀 Starting Sync Talk Kit Backend...

cd /d "%~dp0"

echo 📦 Setting up Python virtual environment...
python -m venv venv

echo 🔧 Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo ⚡ Starting server...
echo Backend will be available at: http://localhost:8000
echo API docs: http://localhost:8000/docs
echo Health check: http://localhost:8000/api/healthz

REM Keep the command prompt open and activated
call venv\Scripts\activate.bat && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
