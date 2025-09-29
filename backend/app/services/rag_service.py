import asyncpg
from typing import List, Dict, Any, Optional
import structlog
import numpy as np
from ..services.supabase_client import supabase_client
from ..core.config import settings

logger = structlog.get_logger()

class RAGService:
    """RAG service for vector search and similarity matching"""

    def __init__(self):
        self.supabase = supabase_client
        self.embedding_dim = 1536  # OpenAI text-embedding-ada-002 dimensions

    async def search_similar_chunks(
        self,
        query: str,
        workbench_id: str,
        limit: int = 5,
        threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Search for similar chunks using vector similarity"""
        try:
            # Generate embedding for the query (placeholder for now)
            query_embedding = await self._generate_query_embedding(query)

            # Perform vector search using pgvector
            pool = await self.supabase.get_pool()

            async with pool.acquire() as conn:
                # Use cosine similarity search
                query_sql = """
                SELECT
                    id,
                    workbench_id,
                    file_id,
                    content,
                    metadata,
                    embedding,
                    1 - (embedding <=> $1::vector) as similarity
                FROM workbench_chunks
                WHERE workbench_id = $2
                AND 1 - (embedding <=> $1::vector) > $3
                ORDER BY embedding <=> $1::vector
                LIMIT $4
                """

                rows = await conn.fetch(
                    query_sql,
                    query_embedding,
                    workbench_id,
                    threshold,
                    limit
                )

                results = []
                for row in rows:
                    results.append({
                        "id": str(row["id"]),
                        "workbench_id": str(row["workbench_id"]),
                        "file_id": str(row["file_id"]),
                        "content": row["content"],
                        "metadata": row["metadata"] or {},
                        "similarity": float(row["similarity"])
                    })

                logger.info("Vector search completed", query_length=len(query), results_count=len(results))
                return results

        except Exception as e:
            logger.error("Error in vector search", error=str(e))
            return []

    async def search_by_keywords(
        self,
        keywords: List[str],
        workbench_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search chunks by keywords using full-text search"""
        try:
            pool = await self.supabase.get_pool()

            async with pool.acquire() as conn:
                # Build search query with multiple keywords
                search_terms = " | ".join(keywords)

                query_sql = """
                SELECT
                    id,
                    workbench_id,
                    file_id,
                    content,
                    metadata,
                    ts_rank_cd(to_tsvector('english', content), plainto_tsquery('english', $1)) as rank
                FROM workbench_chunks
                WHERE workbench_id = $2
                AND to_tsvector('english', content) @@ plainto_tsquery('english', $1)
                ORDER BY rank DESC
                LIMIT $3
                """

                rows = await conn.fetch(query_sql, search_terms, workbench_id, limit)

                results = []
                for row in rows:
                    results.append({
                        "id": str(row["id"]),
                        "workbench_id": str(row["workbench_id"]),
                        "file_id": str(row["file_id"]),
                        "content": row["content"],
                        "metadata": row["metadata"] or {},
                        "rank": float(row["rank"])
                    })

                logger.info("Keyword search completed", keywords=keywords, results_count=len(results))
                return results

        except Exception as e:
            logger.error("Error in keyword search", error=str(e))
            return []

    async def hybrid_search(
        self,
        query: str,
        workbench_id: str,
        limit: int = 5,
        vector_weight: float = 0.7,
        keyword_weight: float = 0.3
    ) -> List[Dict[str, Any]]:
        """Perform hybrid search combining vector and keyword search"""
        try:
            # Extract keywords from query
            keywords = await self._extract_keywords(query)

            # Perform both searches
            vector_results = await self.search_similar_chunks(query, workbench_id, limit * 2)
            keyword_results = await self.search_by_keywords(keywords, workbench_id, limit * 2)

            # Combine and rank results
            combined_results = await self._combine_search_results(
                vector_results, keyword_results, vector_weight, keyword_weight, limit
            )

            logger.info("Hybrid search completed", query_length=len(query), results_count=len(combined_results))
            return combined_results

        except Exception as e:
            logger.error("Error in hybrid search", error=str(e))
            return []

    async def _generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for query text (placeholder implementation)"""
        try:
            # Placeholder: In real implementation, use OpenAI or similar
            # For now, generate random embedding of correct dimensions
            import random
            return [random.random() for _ in range(self.embedding_dim)]

        except Exception as e:
            logger.error("Error generating query embedding", error=str(e))
            return []

    async def _extract_keywords(self, query: str, max_keywords: int = 5) -> List[str]:
        """Extract keywords from query text"""
        try:
            # Simple keyword extraction: split by spaces and filter
            words = query.lower().split()
            # Remove common stop words
            stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
            keywords = [word for word in words if len(word) > 2 and word not in stop_words]

            # Return top keywords
            return keywords[:max_keywords]

        except Exception as e:
            logger.error("Error extracting keywords", error=str(e))
            return []

    async def _combine_search_results(
        self,
        vector_results: List[Dict],
        keyword_results: List[Dict],
        vector_weight: float,
        keyword_weight: float,
        limit: int
    ) -> List[Dict[str, Any]]:
        """Combine vector and keyword search results"""
        try:
            # Create a combined score for each result
            combined_scores = {}

            # Process vector results
            for result in vector_results:
                result_id = result["id"]
                vector_score = result["similarity"]
                combined_scores[result_id] = {
                    "result": result,
                    "vector_score": vector_score,
                    "keyword_score": 0.0,
                    "combined_score": vector_score * vector_weight
                }

            # Process keyword results
            for result in keyword_results:
                result_id = result["id"]
                keyword_score = result["rank"]

                if result_id in combined_scores:
                    # Combine scores
                    combined_scores[result_id]["keyword_score"] = keyword_score
                    combined_scores[result_id]["combined_score"] = (
                        combined_scores[result_id]["vector_score"] * vector_weight +
                        keyword_score * keyword_weight
                    )
                else:
                    # Only keyword match
                    combined_scores[result_id] = {
                        "result": result,
                        "vector_score": 0.0,
                        "keyword_score": keyword_score,
                        "combined_score": keyword_score * keyword_weight
                    }

            # Sort by combined score and return top results
            sorted_results = sorted(
                combined_scores.values(),
                key=lambda x: x["combined_score"],
                reverse=True
            )

            return [item["result"] for item in sorted_results[:limit]]

        except Exception as e:
            logger.error("Error combining search results", error=str(e))
            return []

# Global RAG service instance
rag_service: Optional[RAGService] = None

def get_rag_service() -> RAGService:
    """Get or create RAG service instance"""
    global rag_service
    if rag_service is None:
        rag_service = RAGService()
    return rag_service
