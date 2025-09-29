from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChatSessionCreate(BaseModel):
    workbench_id: str = Field(..., description="ID of the workbench to chat about")
    title: Optional[str] = Field(None, max_length=200)

class ChatSessionResponse(BaseModel):
    session_id: str
    user_id: str
    workbench_id: str
    title: str
    created_at: datetime

class ChatMessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=4000)

class ChatMessageResponse(BaseModel):
    message_id: str
    session_id: str
    sender_id: Optional[str]
    message_type: str
    content: str
    metadata: Dict[str, Any]
    created_at: datetime

class ChatResponse(BaseModel):
    message: str
    context_chunks: List[Dict[str, Any]]
    usage_info: Dict[str, Any]
