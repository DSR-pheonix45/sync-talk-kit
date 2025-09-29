-- 003_workbench_chunks.sql
-- Enable RLS
alter table workbench_chunks enable row level security;

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

-- RLS Policies for workbench_chunks
-- Users can view chunks in workbenches they have access to
create policy "workbench_chunks_select" on workbench_chunks for select using (
  exists (
    select 1 from workbench w
    where w.id = workbench_chunks.workbench_id
    and (w.owner_user_id = auth.uid() or w.id in (
      select wm.workbench_id from workbench_members wm where wm.user_id = auth.uid()
    ))
  )
);

-- Workbench owners and editors can insert chunks (for indexing)
create policy "workbench_chunks_insert" on workbench_chunks for insert with check (
  exists (
    select 1 from workbench w
    where w.id = workbench_chunks.workbench_id
    and (w.owner_user_id = auth.uid() or w.id in (
      select wm.workbench_id from workbench_members wm
      where wm.user_id = auth.uid() and wm.role in ('owner', 'editor')
    ))
  )
);

-- System/service can update chunks (for indexing updates)
create policy "workbench_chunks_update" on workbench_chunks for update using (true);

-- Workbench owners can delete chunks
create policy "workbench_chunks_delete" on workbench_chunks for delete using (
  exists (select 1 from workbench w where w.id = workbench_chunks.workbench_id and w.owner_user_id = auth.uid())
);
