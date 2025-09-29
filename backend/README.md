# Backend API

FastAPI backend for Sync Talk Kit with RAG-powered chat, workbenches, and Supabase integration.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy environment variables:
```bash
cp .env.example .env
```

3. Edit `.env` with your actual values:
- Supabase URL and keys
- Groq API key
- Razorpay credentials
- Redis URL

## Development

Run with auto-reload:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Production

Run with Uvicorn:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Docker

Build and run:
```bash
docker build -t sync-talk-backend .
docker run -p 8000:8000 --env-file .env sync-talk-backend
```

## Database Migrations

Apply migrations to Supabase:
```sql
-- Run the SQL files in backend/db/migrations/ in order
-- 001_enable_pgvector.sql
-- 002_workbench_core.sql
-- 003_workbench_chunks.sql
-- 004_wallet_ledger_counters.sql
```

## API Endpoints

- `GET /api/healthz` - Health check
- `GET /api/readyz` - Readiness check
