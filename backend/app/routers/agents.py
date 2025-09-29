from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import structlog
from ..deps import get_supabase_client, get_user_info
from ..services.agent_service import get_agent_service
from ..models.agent import (
    AgentCreate,
    AgentResponse,
    AgentSessionCreate,
    AgentSessionResponse
)

logger = structlog.get_logger()
router = APIRouter()

@router.post("/agents", response_model=AgentResponse)
async def create_agent(
    agent: AgentCreate,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Create a new AI agent"""
    try:
        agent_service = get_agent_service()

        agent_id = await agent_service.create_agent(user["user_id"], agent)

        # Get the created agent data
        result = supabase.client.table("agent").select("*").eq("agent_id", agent_id).execute()

        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to retrieve created agent")

        logger.info("Agent created", agent_id=agent_id, user_id=user["user_id"])
        return AgentResponse(**result.data[0])

    except Exception as e:
        logger.error("Error creating agent", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to create agent")

@router.get("/agents", response_model=List[AgentResponse])
async def list_agents(
    workbench_id: str = None,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """List available agents"""
    try:
        agent_service = get_agent_service()
        agents = await agent_service.list_agents(user["user_id"], workbench_id)

        return [AgentResponse(**agent) for agent in agents]

    except Exception as e:
        logger.error("Error listing agents", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to list agents")

@router.get("/agents/{agent_id}")
async def get_agent(
    agent_id: str,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Get a specific agent"""
    try:
        agent_service = get_agent_service()
        agent = await agent_service.get_agent(agent_id, user["user_id"])

        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        return AgentResponse(**agent)

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting agent", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get agent")

@router.post("/agents/{agent_id}/query", response_model=AgentSessionResponse)
async def query_agent(
    agent_id: str,
    session: AgentSessionCreate,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Query an agent with a message"""
    try:
        agent_service = get_agent_service()

        response = await agent_service.query_agent(
            agent_id=agent_id,
            user_id=user["user_id"],
            query=session.message
        )

        # Get agent info for response
        agent_result = supabase.client.table("agent").select("*").eq("agent_id", agent_id).execute()

        if not agent_result.data:
            raise HTTPException(status_code=404, detail="Agent not found")

        agent = agent_result.data[0]

        logger.info("Agent queried", agent_id=agent_id, user_id=user["user_id"])
        return AgentSessionResponse(
            session_id=f"session_{agent_id}_{user['user_id']}",
            agent_id=agent_id,
            message=session.message,
            response=response["response"],
            context_chunks=response["context_chunks"],
            metadata=response.get("metadata", {})
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error querying agent", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to query agent")

@router.get("/agents/templates")
async def get_agent_templates():
    """Get available agent types and templates"""
    try:
        # This would return available agent types and their configurations
        return {
            "agent_types": [
                {
                    "type": "dabby_consultant",
                    "name": "Dabby Consultant",
                    "description": "Expert business and financial consultant",
                    "expertise": ["Financial Analysis", "Business Strategy", "Risk Assessment"]
                },
                {
                    "type": "analyser",
                    "name": "Data Analyser",
                    "description": "Specialized in detailed data analysis and insights",
                    "expertise": ["Statistical Analysis", "Trend Analysis", "Performance Metrics"]
                },
                {
                    "type": "generator",
                    "name": "Report Generator",
                    "description": "Professional report generation with multiple formats",
                    "expertise": ["Financial Reports", "Business Reports", "Executive Summaries"]
                }
            ],
            "output_formats": ["pdf", "excel", "word", "html", "json"],
            "report_templates": [
                "financial_summary",
                "business_analysis",
                "executive_summary",
                "detailed_financial",
                "trend_analysis",
                "risk_assessment",
                "strategic_plan",
                "performance_dashboard"
            ]
        }

    except Exception as e:
        logger.error("Error getting agent templates", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get templates")
