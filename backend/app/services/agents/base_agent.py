from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import structlog
from ..services.supabase_client import supabase_client
from ..services.rag_service import get_rag_service

logger = structlog.get_logger()

class BaseAgent(ABC):
    """Base class for all AI agents"""

    def __init__(self, agent_id: str, config: Dict[str, Any]):
        self.agent_id = agent_id
        self.config = config
        self.supabase = supabase_client
        self.rag_service = get_rag_service()

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent type"""
        pass

    @abstractmethod
    def process_query(self, query: str, context_chunks: List[Dict]) -> str:
        """Process a query with context and return response"""
        pass

    async def query(self, message: str, workbench_id: str) -> Dict[str, Any]:
        """Main query method that handles RAG and response generation"""
        try:
            # Get relevant context using RAG
            context_chunks = await self.rag_service.hybrid_search(message, workbench_id)

            # Process query with context
            response = self.process_query(message, context_chunks)

            # Log the interaction
            await self._log_interaction(message, response, context_chunks)

            return {
                "response": response,
                "context_chunks": context_chunks,
                "agent_type": self.__class__.__name__
            }

        except Exception as e:
            logger.error("Error in agent query", agent_id=self.agent_id, error=str(e))
            return {
                "response": "I apologize, but I encountered an error while processing your request. Please try again.",
                "context_chunks": [],
                "agent_type": self.__class__.__name__,
                "error": str(e)
            }

    async def _log_interaction(self, query: str, response: str, context_chunks: List[Dict]):
        """Log agent interaction for analytics"""
        try:
            # This could be extended to store in a dedicated analytics table
            logger.info("Agent interaction", agent_id=self.agent_id, query_length=len(query), response_length=len(response), context_count=len(context_chunks))
        except Exception as e:
            logger.error("Error logging agent interaction", error=str(e))

class AgentFactory:
    """Factory for creating agent instances"""

    _agents: Dict[str, BaseAgent] = {}

    @classmethod
    def get_agent(cls, agent_id: str, agent_type: str, config: Dict[str, Any]) -> BaseAgent:
        """Get or create an agent instance"""
        cache_key = f"{agent_id}_{agent_type}"

        if cache_key not in cls._agents:
            agent_class = cls._get_agent_class(agent_type)
            cls._agents[cache_key] = agent_class(agent_id, config)

        return cls._agents[cache_key]

    @classmethod
    def _get_agent_class(cls, agent_type: str):
        """Get the appropriate agent class"""
        from ..services.agents.dabby_consultant import DabbyConsultantAgent
        from ..services.agents.analyser_agent import AnalyserAgent
        from ..services.agents.generator_agent import GeneratorAgent

        agent_classes = {
            "dabby_consultant": DabbyConsultantAgent,
            "analyser": AnalyserAgent,
            "generator": GeneratorAgent
        }

        return agent_classes.get(agent_type, BaseAgent)

    @classmethod
    def clear_cache(cls):
        """Clear the agent cache"""
        cls._agents.clear()
