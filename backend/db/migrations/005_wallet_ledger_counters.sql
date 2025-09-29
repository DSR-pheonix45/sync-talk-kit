-- 004_wallet_ledger_counters.sql
-- Enable RLS on wallet tables
alter table wallet_usage enable row level security;
alter table wallet_counters enable row level security;

create table if not exists wallet_usage (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(user_id) on delete cascade,
  amount integer not null,   -- negative for deductions, positive for credits
  reason text not null,      -- e.g., 'report', 'chat_bundle', 'purchase'
  reference_id text,         -- payment_id, report_id, session_id, etc.
  created_at timestamptz default now()
);
create index on wallet_usage(user_id);

-- RLS Policies for wallet_usage
-- Users can only view their own wallet usage
create policy "wallet_usage_select" on wallet_usage for select using (user_id = auth.uid());
-- System can insert wallet usage records
create policy "wallet_usage_insert" on wallet_usage for insert with check (true);
-- System can update wallet usage records
create policy "wallet_usage_update" on wallet_usage for update using (true);

create table if not exists wallet_counters (
  user_id uuid primary key references users(user_id) on delete cascade,
  chat_inference_counter integer not null default 0,
  updated_at timestamptz default now()
);

-- RLS Policies for wallet_counters
-- Users can only view their own wallet counters
create policy "wallet_counters_select" on wallet_counters for select using (user_id = auth.uid());
-- System can insert/update wallet counters
create policy "wallet_counters_insert" on wallet_counters for insert with check (true);
create policy "wallet_counters_update" on wallet_counters for update using (true);
