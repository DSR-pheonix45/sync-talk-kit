import asyncio
from typing import Dict, Any, Optional
import structlog
from .supabase_client import supabase_client
from .storage_service import get_storage_service

logger = structlog.get_logger()

class IndexingWorker:
    """Background worker for processing uploaded files"""

    def __init__(self):
        self.supabase = supabase_client
        self.storage = get_storage_service()

    async def process_file(self, file_id: str, workbench_id: str) -> bool:
        """Process an uploaded file: download, chunk, embed, and store"""
        try:
            logger.info("Starting file processing", file_id=file_id, workbench_id=workbench_id)

            # Get file info
            file_result = self.supabase.client.table("workbench_files").select("*").eq("id", file_id).execute()

            if not file_result.data:
                logger.error("File not found", file_id=file_id)
                return False

            file_info = file_result.data[0]
            storage_file_id = file_info.get("storage_file_id")

            if not storage_file_id:
                logger.error("File not found in storage", file_id=file_id)
                await self._update_file_status(file_id, "error", "File not found in storage")
                return False

            # Download file from storage
            file_content = await self._download_file(storage_file_id)
            if not file_content:
                await self._update_file_status(file_id, "error", "Failed to download file")
                return False

            # Extract text based on file type
            text_content = await self._extract_text(file_content, file_info.get("file_type", ""))
            if not text_content:
                await self._update_file_status(file_id, "error", "Failed to extract text")
                return False

            # Chunk the text
            chunks = await self._chunk_text(text_content)

            # Generate embeddings for chunks
            embeddings = await self._generate_embeddings(chunks)

            # Store chunks with embeddings
            await self._store_chunks(workbench_id, file_id, chunks, embeddings)

            # Update file status to indexed
            await self._update_file_status(file_id, "indexed")
            logger.info("File processing completed", file_id=file_id, chunks_count=len(chunks))

            return True

        except Exception as e:
            logger.error("Error processing file", file_id=file_id, error=str(e))
            await self._update_file_status(file_id, "error", str(e))
            return False

    async def _download_file(self, storage_file_id: str) -> Optional[bytes]:
        """Download file from Supabase Storage"""
        try:
            # Get download URL
            url = self.supabase.client.storage.from_("workbench").get_public_url(storage_file_id)

            # Download file
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.content

        except Exception as e:
            logger.error("Error downloading file", storage_file_id=storage_file_id, error=str(e))
            return None

    async def _extract_text(self, file_content: bytes, file_type: str) -> Optional[str]:
        """Extract text from file based on type"""
        try:
            if file_type == "text/plain":
                return file_content.decode("utf-8")
            elif file_type == "application/pdf":
                # Use pypdf for PDF extraction
                from io import BytesIO
                from pypdf import PdfReader

                pdf_file = BytesIO(file_content)
                pdf_reader = PdfReader(pdf_file)

                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"

                return text
            elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                              "application/msword"]:
                # Use docx2txt for Word documents
                import docx2txt
                from io import BytesIO

                docx_file = BytesIO(file_content)
                return docx2txt.process(docx_file)
            else:
                logger.warning("Unsupported file type for text extraction", file_type=file_type)
                return None

        except Exception as e:
            logger.error("Error extracting text", file_type=file_type, error=str(e))
            return None

    async def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
        """Split text into chunks"""
        try:
            words = text.split()
            chunks = []

            for i in range(0, len(words), chunk_size - overlap):
                chunk_words = words[i:i + chunk_size]
                chunks.append(" ".join(chunk_words))

            return chunks

        except Exception as e:
            logger.error("Error chunking text", error=str(e))
            return []

    async def _generate_embeddings(self, chunks: list[str]) -> list[list[float]]:
        """Generate embeddings for text chunks"""
        try:
            # Placeholder for embedding generation
            # In real implementation, you'd use OpenAI, SentenceTransformers, or similar
            logger.info("Generating embeddings", chunks_count=len(chunks))

            # For now, return placeholder embeddings (1536 dimensions for OpenAI text-embedding-ada-002)
            import random
            return [[random.random() for _ in range(1536)] for _ in chunks]

        except Exception as e:
            logger.error("Error generating embeddings", error=str(e))
            return []

    async def _store_chunks(self, workbench_id: str, file_id: str, chunks: list[str], embeddings: list[list[float]]):
        """Store chunks with embeddings in the database"""
        try:
            chunk_data = []

            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                chunk_data.append({
                    "workbench_id": workbench_id,
                    "file_id": file_id,
                    "chunk_id": f"{file_id}_{i}",
                    "content": chunk,
                    "metadata": {"chunk_index": i, "total_chunks": len(chunks)},
                    "embedding": embedding
                })

            # Insert chunks in batches
            batch_size = 100
            for i in range(0, len(chunk_data), batch_size):
                batch = chunk_data[i:i + batch_size]
                result = self.supabase.client.table("workbench_chunks").insert(batch).execute()

                if not result.data:
                    raise Exception(f"Failed to insert chunk batch {i//batch_size}")

            logger.info("Stored chunks", chunks_count=len(chunks))

        except Exception as e:
            logger.error("Error storing chunks", error=str(e))
            raise

    async def _update_file_status(self, file_id: str, status: str, error_message: Optional[str] = None):
        """Update file processing status"""
        try:
            update_data = {"status": status}
            if error_message:
                update_data["error_message"] = error_message

            self.supabase.client.table("workbench_files").update(update_data).eq("id", file_id).execute()

        except Exception as e:
            logger.error("Error updating file status", file_id=file_id, error=str(e))

# Global worker instance
indexing_worker: Optional[IndexingWorker] = None

def get_indexing_worker() -> IndexingWorker:
    """Get or create indexing worker instance"""
    global indexing_worker
    if indexing_worker is None:
        indexing_worker = IndexingWorker()
    return indexing_worker
