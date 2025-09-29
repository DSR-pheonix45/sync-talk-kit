from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class AgentType(str, Enum):
    DABBY_CONSULTANT = "dabby_consultant"
    ANALYSER = "analyser"
    GENERATOR = "generator"

class AgentPersona(str, Enum):
    CONSULTANT = "consultant"
    ANALYST = "analyst"
    GENERATOR = "generator"

class AgentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    agent_type: AgentType
    workbench_id: str
    config: Optional[Dict[str, Any]] = None

class AgentResponse(BaseModel):
    agent_id: str
    name: str
    description: Optional[str]
    agent_type: AgentType
    workbench_id: str
    config: Dict[str, Any]
    created_at: datetime

class AgentSessionCreate(BaseModel):
    agent_id: str
    message: str = Field(..., min_length=1, max_length=4000)

class AgentSessionResponse(BaseModel):
    session_id: str
    agent_id: str
    message: str
    response: str
    context_chunks: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    created_at: datetime
