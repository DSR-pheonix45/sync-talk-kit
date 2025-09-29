from supabase import create_client, Client
import asyncpg
from typing import Optional
import structlog
from .config import settings

logger = structlog.get_logger()

class SupabaseClient:
    def __init__(self):
        self.url = settings.supabase_url
        self.anon_key = settings.supabase_anon_key
        self.service_role_key = settings.supabase_service_role_key
        self.client: Client = create_client(self.url, self.anon_key)
        self._pool: Optional[asyncpg.Pool] = None

    async def get_pool(self) -> asyncpg.Pool:
        """Get asyncpg connection pool for vector operations"""
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                settings.supabase_url.replace("https://", "postgresql://").replace("http://", "postgresql://") +
                "?sslmode=require",
                user=self.service_role_key,
                password=self.service_role_key,
                database="postgres"
            )
        return self._pool

    async def close(self):
        """Close the connection pool"""
        if self._pool:
            await self._pool.close()

supabase_client = SupabaseClient()
