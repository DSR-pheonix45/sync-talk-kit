from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str
    supabase_jwt_secret: str
    supabase_storage_bucket: str = "workbench"

    groq_api_key: str

    razorpay_key_id: str
    razorpay_key_secret: str
    razorpay_webhook_secret: str

    redis_url: str = "redis://redis:6379/0"

    app_env: str = "prod"
    log_level: str = "info"

    class Config:
        env_file = ".env"

settings = Settings()
