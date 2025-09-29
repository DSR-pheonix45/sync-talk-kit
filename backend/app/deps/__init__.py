from fastapi import Depends
from .services.supabase_client import supabase_client, SupabaseClient
from .core.auth import get_current_user
from typing import Dict, Any

async def get_supabase_client() -> SupabaseClient:
    """Dependency to get Supabase client"""
    return supabase_client

async def get_user_info(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Dependency to get current user info"""
    return user

# Rate limiting dependency (placeholder for now)
async def rate_limit(user: Dict[str, Any] = Depends(get_user_info)):
    """Rate limiting logic - to be implemented"""
    # TODO: Implement rate limiting per user/IP
    pass
