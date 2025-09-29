from typing import List, Dict, Any, Optional
import structlog
import asyncio
from ..services.supabase_client import supabase_client
from ..services.rag_service import get_rag_service
from ..core.config import settings

logger = structlog.get_logger()

class ChatService:
    """Chat service with LLM integration and session management"""

    def __init__(self):
        self.supabase = supabase_client
        self.rag_service = get_rag_service()

    async def create_session(
        self,
        user_id: str,
        workbench_id: str,
        title: Optional[str] = None
    ) -> str:
        """Create a new chat session"""
        try:
            session_data = {
                "user_id": user_id,
                "workbench_id": workbench_id,
                "title": title or f"Chat Session {user_id[:8]}"
            }

            result = self.supabase.client.table("session").insert(session_data).execute()

            if not result.data:
                raise Exception("Failed to create chat session")

            session_id = result.data[0]["session_id"]
            logger.info("Created chat session", session_id=session_id, user_id=user_id)
            return session_id

        except Exception as e:
            logger.error("Error creating chat session", error=str(e))
            raise

    async def send_message(
        self,
        session_id: str,
        user_id: str,
        message: str,
        workbench_id: str
    ) -> Dict[str, Any]:
        """Send a message and get AI response"""
        try:
            # Verify session access
            await self._verify_session_access(session_id, user_id, workbench_id)

            # Store user message
            await self._store_message(session_id, user_id, "user", message)

            # Search for relevant context
            context_chunks = await self.rag_service.hybrid_search(message, workbench_id)

            # Generate AI response
            ai_response = await self._generate_ai_response(message, context_chunks, workbench_id)

            # Store AI response
            await self._store_message(session_id, "system", "assistant", ai_response)

            # Update session usage counter
            await self._update_usage_counter(user_id)

            logger.info("Chat message processed", session_id=session_id, message_length=len(message))
            return {
                "message": ai_response,
                "context_chunks": context_chunks,
                "usage_info": {
                    "tokens_used": len(ai_response.split()) * 1.3,  # Rough estimate
                    "context_chunks": len(context_chunks)
                }
            }

        except Exception as e:
            logger.error("Error processing chat message", error=str(e))
            raise

    async def get_session_messages(
        self,
        session_id: str,
        user_id: str,
        workbench_id: str
    ) -> List[Dict[str, Any]]:
        """Get messages for a chat session"""
        try:
            # Verify session access
            await self._verify_session_access(session_id, user_id, workbench_id)

            result = self.supabase.client.table("message").select("*").eq("session_id", session_id).order("created_at").execute()

            messages = []
            for msg in result.data:
                messages.append({
                    "id": str(msg["message_id"]),
                    "session_id": str(msg["session_id"]),
                    "sender_id": str(msg["sender_id"]) if msg["sender_id"] else None,
                    "message_type": msg["message_type"],
                    "content": msg["content"],
                    "metadata": msg["metadata"] or {},
                    "created_at": msg["created_at"]
                })

            return messages

        except Exception as e:
            logger.error("Error getting session messages", error=str(e))
            return []

    async def _verify_session_access(self, session_id: str, user_id: str, workbench_id: str):
        """Verify user has access to the session and workbench"""
        # Check if session exists and user has access to the workbench
        session_result = self.supabase.client.table("session").select("*").eq("session_id", session_id).execute()

        if not session_result.data:
            raise Exception("Session not found")

        session = session_result.data[0]

        if session["user_id"] != user_id:
            raise Exception("Access denied to session")

        if session["workbench_id"] != workbench_id:
            raise Exception("Session does not belong to this workbench")

    async def _store_message(
        self,
        session_id: str,
        sender_id: str,
        message_type: str,
        content: str,
        metadata: Optional[Dict] = None
    ):
        """Store a message in the database"""
        try:
            message_data = {
                "session_id": session_id,
                "sender_id": sender_id if message_type == "user" else None,
                "message_type": message_type,
                "content": content,
                "metadata": metadata or {}
            }

            self.supabase.client.table("message").insert(message_data).execute()

        except Exception as e:
            logger.error("Error storing message", error=str(e))

    async def _generate_ai_response(
        self,
        user_message: str,
        context_chunks: List[Dict],
        workbench_id: str
    ) -> str:
        """Generate AI response using context and LLM"""
        try:
            # Build context from chunks
            context_text = self._build_context_text(context_chunks)

            # Create system prompt
            system_prompt = self._create_system_prompt(workbench_id, context_text)

            # Generate response using Groq (placeholder)
            response = await self._call_llm(system_prompt, user_message)

            return response

        except Exception as e:
            logger.error("Error generating AI response", error=str(e))
            return "I apologize, but I encountered an error while processing your request. Please try again."

    def _build_context_text(self, context_chunks: List[Dict]) -> str:
        """Build context text from search results"""
        if not context_chunks:
            return ""

        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            context_parts.append(f"[Source {i}] {chunk['content']}")

        return "\n\n".join(context_parts)

    def _create_system_prompt(self, workbench_id: str, context: str) -> str:
        """Create system prompt for the LLM"""
        base_prompt = """You are a helpful AI assistant specialized in analyzing business and financial data. You have access to relevant information from uploaded documents.

When answering questions:
1. Be specific and cite your sources when possible
2. Use the provided context to inform your response
3. If you don't have enough information, clearly state your limitations
4. Focus on accuracy and relevance to the user's query

"""

        if context:
            base_prompt += f"\nRelevant context from documents:\n{context}\n"

        return base_prompt

    async def _call_llm(self, system_prompt: str, user_message: str) -> str:
        """Call LLM API (Groq) to generate response"""
        try:
            # Placeholder for Groq API call
            # In real implementation, you'd use the Groq client

            # Simulate LLM response
            await asyncio.sleep(0.1)  # Simulate API delay

            # Mock response based on message content
            if "financial" in user_message.lower() or "revenue" in user_message.lower():
                return "Based on the available financial data, I can help you analyze revenue trends and projections. The context shows several key financial metrics that might be relevant to your analysis."
            elif "analysis" in user_message.lower():
                return "I'll analyze the available data to provide insights. From the context provided, I can identify several key patterns and trends that may be useful for your decision-making."
            else:
                return "I understand your question. Let me provide a comprehensive response based on the available context and data analysis."

        except Exception as e:
            logger.error("Error calling LLM", error=str(e))
            return "I'm currently unable to process your request due to a technical issue. Please try again later."

    async def _update_usage_counter(self, user_id: str):
        """Update user's chat inference counter"""
        try:
            # Get current counter
            result = self.supabase.client.table("wallet_counters").select("*").eq("user_id", user_id).execute()

            if result.data:
                # Update existing counter
                current_count = result.data[0]["chat_inference_counter"] + 1
                self.supabase.client.table("wallet_counters").update({
                    "chat_inference_counter": current_count,
                    "updated_at": "now()"
                }).eq("user_id", user_id).execute()
            else:
                # Create new counter
                self.supabase.client.table("wallet_counters").insert({
                    "user_id": user_id,
                    "chat_inference_counter": 1
                }).execute()

        except Exception as e:
            logger.error("Error updating usage counter", error=str(e))

# Global chat service instance
chat_service: Optional[ChatService] = None

def get_chat_service() -> ChatService:
    """Get or create chat service instance"""
    global chat_service
    if chat_service is None:
        chat_service = ChatService()
    return chat_service
