from typing import Dict, Any, List, Optional
import structlog
from ..services.supabase_client import supabase_client
from ..services.agents.base_agent import AgentFactory
from ..models.agent import AgentType, AgentCreate, AgentResponse

logger = structlog.get_logger()

class AgentService:
    """Service for managing AI agents"""

    def __init__(self):
        self.supabase = supabase_client
        self.agent_factory = AgentFactory()

    async def create_agent(
        self,
        user_id: str,
        agent_data: AgentCreate
    ) -> str:
        """Create a new agent instance"""
        try:
            # Store agent configuration
            agent_config = {
                "name": agent_data.name,
                "description": agent_data.description,
                "agent_type": agent_data.agent_type,
                "workbench_id": agent_data.workbench_id,
                "config": agent_data.config or {}
            }

            result = self.supabase.client.table("agent").insert(agent_config).execute()

            if not result.data:
                raise Exception("Failed to create agent")

            agent_id = result.data[0]["agent_id"]
            logger.info("Created agent", agent_id=agent_id, user_id=user_id, agent_type=agent_data.agent_type)

            return agent_id

        except Exception as e:
            logger.error("Error creating agent", error=str(e))
            raise

    async def get_agent(self, agent_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get agent configuration"""
        try:
            result = self.supabase.client.table("agent").select("*").eq("agent_id", agent_id).execute()

            if not result.data:
                return None

            agent = result.data[0]

            # Verify user has access to the workbench
            await self._verify_workbench_access(agent["workbench_id"], user_id)

            return agent

        except Exception as e:
            logger.error("Error getting agent", error=str(e))
            return None

    async def list_agents(self, user_id: str, workbench_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List available agents for user"""
        try:
            query = self.supabase.client.table("agent").select("*")

            if workbench_id:
                query = query.eq("workbench_id", workbench_id)

            result = query.execute()

            agents = []
            for agent in result.data:
                # Verify access to workbench
                try:
                    await self._verify_workbench_access(agent["workbench_id"], user_id)
                    agents.append(agent)
                except:
                    continue  # Skip agents user doesn't have access to

            return agents

        except Exception as e:
            logger.error("Error listing agents", error=str(e))
            return []

    async def query_agent(
        self,
        agent_id: str,
        user_id: str,
        query: str
    ) -> Dict[str, Any]:
        """Query an agent with a message"""
        try:
            # Get agent configuration
            agent = await self.get_agent(agent_id, user_id)

            if not agent:
                raise Exception("Agent not found or access denied")

            # Get agent instance
            agent_instance = self.agent_factory.get_agent(
                agent_id=agent_id,
                agent_type=agent["agent_type"],
                config=agent["config"]
            )

            # Get workbench context
            workbench_id = agent["workbench_id"]

            # Process query
            response = await agent_instance.query(query, workbench_id)

            # Store interaction for analytics
            await self._store_interaction(agent_id, user_id, query, response)

            return {
                "agent_id": agent_id,
                "agent_name": agent["name"],
                "agent_type": agent["agent_type"],
                "query": query,
                "response": response["response"],
                "context_chunks": response["context_chunks"],
                "metadata": response.get("metadata", {})
            }

        except Exception as e:
            logger.error("Error querying agent", agent_id=agent_id, error=str(e))
            raise

    async def _verify_workbench_access(self, workbench_id: str, user_id: str):
        """Verify user has access to workbench"""
        result = self.supabase.client.table("workbench").select("*").eq("id", workbench_id).execute()

        if not result.data:
            raise Exception("Workbench not found")

        workbench = result.data[0]

        # Check if user is owner
        if workbench["owner_user_id"] == user_id:
            return

        # Check if user is a member
        member_result = self.supabase.client.table("workbench_members").select("*").eq("workbench_id", workbench_id).eq("user_id", user_id).execute()

        if not member_result.data:
            raise Exception("Access denied to workbench")

    async def _store_interaction(self, agent_id: str, user_id: str, query: str, response: Dict[str, Any]):
        """Store agent interaction for analytics"""
        try:
            interaction_data = {
                "agent_id": agent_id,
                "user_id": user_id,
                "query": query,
                "response_length": len(response.get("response", "")),
                "context_chunks_used": len(response.get("context_chunks", [])),
                "agent_type": response.get("agent_type", "unknown")
            }

            # This would typically go to an analytics table
            logger.info("Agent interaction stored", **interaction_data)

        except Exception as e:
            logger.error("Error storing interaction", error=str(e))

# Global agent service instance
agent_service: Optional[AgentService] = None

def get_agent_service() -> AgentService:
    """Get or create agent service instance"""
    global agent_service
    if agent_service is None:
        agent_service = AgentService()
    return agent_service
