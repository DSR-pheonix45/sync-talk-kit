Implementation Plan (FastAPI + Supabase + pgvector + Groq + Razorpay)
Overview
Backend: FastAPI (Python), Uvicorn ASGI.
DB: Supabase Postgres with pgvector, existing tables leveraged (users, wallet, subscription, company, storage, reports, session, message).
Vector Store: pgvector on Supabase.
Storage: Supabase Storage buckets.
LLM: Groq Cloud chat models (e.g., Llama 3.1).
Queue/Workers: Redis + RQ/Celery for preprocessing and report generation.
Payments: Razorpay orders + webhook.
Deploy: Docker + Cloud Run (GCP).
Observability: Structured logs, optional Sentry, Prometheus-compatible metrics.
Directory Layout
backend/
  app/
    main.py
    core/               # config, logging, security deps, error handlers
    deps/               # DB clients, auth dependency, rate limit
    models/             # Pydantic request/response schemas
    routers/            # FastAPI routers per domain
      auth.py
      wallet.py
      payments.py
      companies.py
      workbenches.py
      rag.py
      chat.py
      reports.py
      health.py
    services/           # business logic components
      supabase_client.py
      storage_service.py
      workbench_service.py
      rag_indexer.py
      rag_query.py
      groq_client.py
      credits_service.py
      payments_service.py
      report_service.py
    workers/
      worker.py         # queue consumers: indexing, report generation
    db/
      migrations/       # SQL files (pgvector, tables, indices)
  requirements.txt
  dockerfile
  .env.example
  README.md
  Implementation.md
Environment Variables (.env)
SUPABASE_URL=
SUPABASE_ANON_KEY=                      # only for local dev if needed
SUPABASE_SERVICE_ROLE_KEY=              # server-side privileged
SUPABASE_JWT_SECRET=                    # verify Supabase JWTs

SUPABASE_STORAGE_BUCKET=workbench       # create via Supabase Console or SQL

GROQ_API_KEY=

RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
RAZORPAY_WEBHOOK_SECRET=

REDIS_URL=redis://redis:6379/0

APP_ENV=prod
LOG_LEVEL=info
Phase 0 — Prerequisites
Create Supabase project, obtain URL/keys.
Enable pgvector:
Ensure extension enabled in your Supabase project.
Create Storage bucket for workbench files and for generated reports.
Provision Redis (Cloud Memorystore or managed Redis).
Phase 1 — Database Schema (SQL Migrations)
Add new tables (workbench domain + RAG + wallet usage + counters). Reuse existing tables wherever possible.

sql
-- 001_enable_pgvector.sql
create extension if not exists vector;

-- 002_workbench_core.sql
create table if not exists workbench (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  description text,
  owner_user_id uuid references users(user_id) on delete set null,
  company_id text references company(company_id) on delete set null,
  created_at timestamptz default now()
);
create index on workbench(owner_user_id);
create index on workbench(company_id);

create table if not exists workbench_members (
  id uuid primary key default gen_random_uuid(),
  workbench_id uuid references workbench(id) on delete cascade,
  user_id uuid references users(user_id) on delete cascade,
  role text not null check (role in ('owner','editor','viewer')),
  created_at timestamptz default now()
);
create unique index on workbench_members(workbench_id, user_id);

create table if not exists workbench_files (
  id uuid primary key default gen_random_uuid(),
  workbench_id uuid references workbench(id) on delete cascade,
  storage_file_id text,  -- references storage.file_id logically
  file_name text not null,
  file_type text,
  size_bytes bigint,
  status text not null default 'pending' check (status in ('pending','indexed','error')),
  error_message text,
  created_at timestamptz default now()
);
create index on workbench_files(workbench_id);

-- 003_workbench_chunks.sql
create table if not exists workbench_chunks (
  id uuid primary key default gen_random_uuid(),
  workbench_id uuid references workbench(id) on delete cascade,
  file_id uuid references workbench_files(id) on delete cascade,
  chunk_id text,
  content text not null,
  metadata jsonb,
  embedding vector(1536)  -- adjust dims to embedding model used
);
create index on workbench_chunks(workbench_id);
-- cosine similarity index
create index workbench_chunks_embedding_ivfflat on workbench_chunks using ivfflat (embedding vector_cosine_ops) with (lists = 100);

-- 004_wallet_ledger_counters.sql
create table if not exists wallet_usage (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(user_id) on delete cascade,
  amount integer not null,   -- negative for deductions, positive for credits
  reason text not null,      -- e.g., 'report', 'chat_bundle', 'purchase'
  reference_id text,         -- payment_id, report_id, session_id, etc.
  created_at timestamptz default now()
);
create index on wallet_usage(user_id);

create table if not exists wallet_counters (
  user_id uuid primary key references users(user_id) on delete cascade,
  chat_inference_counter integer not null default 0,
  updated_at timestamptz default now()
);
Notes:

We can also add a seats int column to subscription or keep it in wallet.
Existing reports and storage tables are used for generated artifacts and raw files metadata.
Phase 2 — FastAPI Scaffold
app/main.py: create FastAPI app, include routers, load env, configure logging and CORS for the frontend origin.
app/core/auth.py: Supabase JWT validation dependency.
app/services/supabase_client.py: PostgREST client or supabase-py client for CRUD. For pgvector queries, use asyncpg directly.
app/routers/health.py: GET /healthz.
Phase 3 — Auth
Supabase JWT verification for Bearer tokens in Authorization header.
Dependency get_current_user() returns user_id/email or raises 401.
Guard endpoints for user/company access.
Phase 4 — Workbench API
Endpoints:

POST /workbenches → create personal or company workbench.
GET /workbenches?companyId= → list visible workbenches.
POST /workbenches/{id}/files → multipart upload; proxy to Supabase Storage; create workbench_files; enqueue indexing.
GET /workbenches/{id}/files → list files with status.
GET /workbenches/{id}/status → summarised indexing state and errors.
Access control rules:

Owner and workbench_members roles.
For company workbenches, membership inferred from company_members plus explicit overrides in workbench_members.
Phase 5 — Indexing Pipeline (Analyst Agent)
Worker jobs:

Download file via signed URL.
Extract text by type: pdf (pypdf), docx (docx2txt), xlsx/csv (pandas), txt.
Clean, chunk (e.g., 800 tokens, 200 overlap).
Embed chunks (SentenceTransformers or Groq embeddings when available).
Upsert workbench_chunks with embeddings and metadata.
Update workbench_files.status to indexed or error (with error_message).
Error surfaces: Chat will call /workbenches/{id}/status and include issues in the assistant response.
Phase 6 — RAG + Chat
Endpoints:

POST /chat/sessions → create session or reuse active.
POST /chat/sessions/{id}/messages:
Validate workbench access.
Run preflight: check workbench_files for errors/missing files (if user specifies dependencies).
Embed query → vector search in workbench_chunks by workbench_id.
Build CFO persona prompt with sources and KPIs scaffold.
Call Groq LLM; stream if possible; save user+assistant messages to public.message.
Credit accounting: increment chat_inference_counter. On 10th message, deduct 1 credit, reset counter and log in wallet_usage.
GET /chat/sessions/{id}/messages → history.
Phase 7 — Credits & Wallet
GET /wallet → current balance, plan, counters, usage summary.
Internal service method:
credits_service.deduct(user_id, amount, reason, reference_id) transactional, idempotent (idempotency key optional).
credits_service.increment_counter(user_id) and auto-deduct 1 credit on every 10th chat inference.
Update wallet, write wallet_usage, and maintain wallet_counters.
Phase 8 — Payments (Razorpay)
GET /plans → list lite/pro/enterprise (enterprise marked “contact”).
POST /checkout/session → create Razorpay order, return order_id, amount, currency.
POST /webhooks/razorpay:
Verify signature.
On successful payment, credit wallet: +100 for lite, +400 for pro; set plan; add 1 seat for pro; log wallet_usage with reason purchase.
Idempotent by payment_id.
Enterprise: admin tool later to set custom credits/seats.
Phase 9 — Reports
POST /reports → inputs: workbench_id, report_type, title, notes.
Validate prerequisites (template required files present).
If missing, respond with actionable errors (also visible in chat).
Enqueue job, deduct 1 credit (idempotent per request id).
Worker:
Use RAG to assemble data, compute KPIs, fill Jinja2/Markdown template.
Render PDF/Doc/Excel as needed.
Upload to Supabase Storage; insert row in public.reports with download_url.
GET /reports?workbenchId=
GET /reports/{id}
Phase 10 — Observability
Structured logs (json).
Request IDs and correlation IDs.
Optional Sentry integration.
Health endpoints: /healthz (liveness), /readyz (readiness).
Phase 11 — Security, Rate Limit, Idempotency
Rate limit per IP and per user for chat endpoints.
Idempotency header (Idempotency-Key) on credit-deducting endpoints, stored in a small table to avoid duplicates.
Harden CORS to frontend origin.
Phase 12 — CI/CD and Testing
Tests:
Unit tests for services (credits, rag chunking).
Integration tests for routers (httpx + test containers).
CI:
GitHub Actions: lint, test, build Docker, push to Artifact Registry, deploy to Cloud Run.
Secrets in GitHub: use workload identity or encrypted secrets.
Phase 13 — Deployment to Cloud Run
Build Docker:
Multi-stage: poetry/pip install → slim runtime.
Cloud Run:
CPU: 1–2, memory: 1–2GB to start.
Min instances: 0–1, max as needed.
Configure env vars from Secret Manager.
Allow only HTTPS; set concurrency ~80 for FastAPI.
Redis: GCP Memorystore (VPC), or external managed Redis with TLS.
Supabase: internet egress allowed; secure keys via secrets.
Phase 14 — Frontend Wiring (No UI Changes)
CompanyModal.tsx
 → POST /companies on submit.
WorkbenchModal.tsx
 → POST /workbenches then upload each file to /workbenches/{id}/files; poll /workbenches/{id}/files.
ReportModal.tsx
 → POST /reports; show job state.
ChatInput.tsx
 → POST /chat/sessions/{id}/messages; render assistant message + sources.
Sidebar credits → GET /wallet; Upgrade Plan → POST /checkout/session.
API Summary
Auth: Supabase JWT in Authorization: Bearer <token>
Companies: POST /companies, GET /companies, PATCH /companies/{id}
Workbenches: POST /workbenches, GET /workbenches, POST /workbenches/{id}/files, GET /workbenches/{id}/files, GET /workbenches/{id}/status
Chat: POST /chat/sessions, POST /chat/sessions/{id}/messages, GET /chat/sessions/{id}/messages
Wallet: GET /wallet
Payments: GET /plans, POST /checkout/session, POST /webhooks/razorpay
Reports: POST /reports, GET /reports, GET /reports/{id}
Health: GET /healthz, GET /readyz
Acceptance Criteria per Phase
Phase 1: Migrations apply cleanly; pgvector indexes present.
Phase 4–5: Upload → file rows created → indexing job completes → status=indexed and chunks searchable.
Phase 6: Chat returns answers with citations and handles missing files gracefully.
Phase 7–8: Credits reflect purchases, deductions happen as per rules. Webhook idempotency proven.
Phase 9: Report generated and downloadable, credit deducted once.
Phase 13: Cloud Run deploy stable under basic load; logs and metrics visible.
Timeline (suggested)
Week 1: Phases 1–3 (schema, scaffold, auth).
Week 2: Phases 4–6 (workbench, indexing, RAG chat).
Week 3: Phases 7–9 (credits, payments, reports).
Week 4: Phases 10–14 (obs, security, CI/CD, Cloud Run, frontend wiring, QA).