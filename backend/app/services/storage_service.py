from supabase import Client
from typing import Optional
import structlog

logger = structlog.get_logger()

class StorageService:
    def __init__(self, supabase_client: Client, bucket_name: str = "workbench"):
        self.client = supabase_client
        self.bucket_name = bucket_name

    async def upload_file(self, file_path: str, file_content: bytes, content_type: str) -> Optional[str]:
        """Upload a file to Supabase Storage and return the file ID"""
        try:
            # Generate unique filename
            import uuid
            file_extension = file_path.split('.')[-1] if '.' in file_path else ''
            storage_filename = f"{uuid.uuid4()}.{file_extension}"

            # Upload to storage
            result = self.client.storage.from_(self.bucket_name).upload(
                storage_filename,
                file_content,
                {"content-type": content_type}
            )

            if result.get("error"):
                logger.error("Failed to upload file to storage", error=result["error"])
                return None

            return storage_filename

        except Exception as e:
            logger.error("Error uploading file", error=str(e))
            return None

    async def get_public_url(self, file_id: str) -> Optional[str]:
        """Get public URL for a file"""
        try:
            url = self.client.storage.from_(self.bucket_name).get_public_url(file_id)
            return url
        except Exception as e:
            logger.error("Error getting public URL", error=str(e))
            return None

    async def delete_file(self, file_id: str) -> bool:
        """Delete a file from storage"""
        try:
            result = self.client.storage.from_(self.bucket_name).remove([file_id])
            return not result.get("error", False)
        except Exception as e:
            logger.error("Error deleting file", error=str(e))
            return False

# Global storage service instance
storage_service: Optional[StorageService] = None

def get_storage_service() -> StorageService:
    """Get or create storage service instance"""
    return storage_service

def init_storage_service(supabase_client: Client, bucket_name: str = "workbench"):
    """Initialize storage service"""
    global storage_service
    storage_service = StorageService(supabase_client, bucket_name)
