-- 002_workbench_core.sql
-- Enable RLS on all tables
alter table workbench enable row level security;
alter table workbench_members enable row level security;
alter table workbench_files enable row level security;

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

-- RLS Policies for workbench
-- Users can view workbenches they own or are members of
create policy "workbench_select" on workbench for select using (
  owner_user_id = auth.uid() or
  exists (
    select 1 from workbench_members wm
    where wm.workbench_id = workbench.id and wm.user_id = auth.uid()
  )
);

-- Users can insert workbenches (they become owners)
create policy "workbench_insert" on workbench for insert with check (owner_user_id = auth.uid());

-- Owners can update their workbenches
create policy "workbench_update" on workbench for update using (owner_user_id = auth.uid());

-- Owners can delete their workbenches
create policy "workbench_delete" on workbench for delete using (owner_user_id = auth.uid());

create table if not exists workbench_members (
  id uuid primary key default gen_random_uuid(),
  workbench_id uuid references workbench(id) on delete cascade,
  user_id uuid references users(user_id) on delete cascade,
  role text not null check (role in ('owner','editor','viewer')),
  created_at timestamptz default now()
);
create unique index on workbench_members(workbench_id, user_id);

-- RLS Policies for workbench_members
-- Users can view memberships for workbenches they have access to
create policy "workbench_members_select" on workbench_members for select using (
  exists (
    select 1 from workbench w
    where w.id = workbench_members.workbench_id
    and (w.owner_user_id = auth.uid() or w.id in (
      select wm.workbench_id from workbench_members wm where wm.user_id = auth.uid()
    ))
  )
);

-- Workbench owners can manage members
create policy "workbench_members_insert" on workbench_members for insert with check (
  exists (select 1 from workbench w where w.id = workbench_id and w.owner_user_id = auth.uid())
);

-- Workbench owners can update member roles
create policy "workbench_members_update" on workbench_members for update using (
  exists (select 1 from workbench w where w.id = workbench_id and w.owner_user_id = auth.uid())
);

-- Workbench owners can remove members
create policy "workbench_members_delete" on workbench_members for delete using (
  exists (select 1 from workbench w where w.id = workbench_id and w.owner_user_id = auth.uid())
);

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

-- RLS Policies for workbench_files
-- Users can view files in workbenches they have access to
create policy "workbench_files_select" on workbench_files for select using (
  exists (
    select 1 from workbench w
    where w.id = workbench_files.workbench_id
    and (w.owner_user_id = auth.uid() or w.id in (
      select wm.workbench_id from workbench_members wm where wm.user_id = auth.uid()
    ))
  )
);

-- Workbench owners and editors can upload files
create policy "workbench_files_insert" on workbench_files for insert with check (
  exists (
    select 1 from workbench w
    where w.id = workbench_files.workbench_id
    and (w.owner_user_id = auth.uid() or w.id in (
      select wm.workbench_id from workbench_members wm
      where wm.user_id = auth.uid() and wm.role in ('owner', 'editor')
    ))
  )
);

-- Workbench owners and editors can update file status
create policy "workbench_files_update" on workbench_files for update using (
  exists (
    select 1 from workbench w
    where w.id = workbench_files.workbench_id
    and (w.owner_user_id = auth.uid() or w.id in (
      select wm.workbench_id from workbench_members wm
      where wm.user_id = auth.uid() and wm.role in ('owner', 'editor')
    ))
  )
);

-- Workbench owners can delete files
create policy "workbench_files_delete" on workbench_files for delete using (
  exists (select 1 from workbench w where w.id = workbench_files.workbench_id and w.owner_user_id = auth.uid())
);
