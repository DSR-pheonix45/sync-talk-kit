from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import structlog
from ..deps import get_supabase_client, get_user_info
from ..services.chat_service import get_chat_service
from ..models.chat import (
    ChatSessionCreate,
    ChatSessionResponse,
    ChatMessageCreate,
    ChatMessageResponse,
    ChatResponse
)

logger = structlog.get_logger()
router = APIRouter()

@router.post("/chat/sessions", response_model=ChatSessionResponse)
async def create_chat_session(
    session: ChatSessionCreate,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Create a new chat session"""
    try:
        chat_service = get_chat_service()

        session_id = await chat_service.create_session(
            user_id=user["user_id"],
            workbench_id=session.workbench_id,
            title=session.title
        )

        # Get the created session data
        result = supabase.client.table("session").select("*").eq("session_id", session_id).execute()

        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to retrieve created session")

        return ChatSessionResponse(**result.data[0])

    except Exception as e:
        logger.error("Error creating chat session", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to create chat session")

@router.post("/chat/sessions/{session_id}/messages", response_model=ChatResponse)
async def send_chat_message(
    session_id: str,
    message: ChatMessageCreate,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Send a message in a chat session"""
    try:
        chat_service = get_chat_service()

        # Get session info to extract workbench_id
        session_result = supabase.client.table("session").select("*").eq("session_id", session_id).execute()

        if not session_result.data:
            raise HTTPException(status_code=404, detail="Chat session not found")

        session_data = session_result.data[0]
        workbench_id = session_data["workbench_id"]

        # Process the message
        response_data = await chat_service.send_message(
            session_id=session_id,
            user_id=user["user_id"],
            message=message.content,
            workbench_id=workbench_id
        )

        logger.info("Chat message sent", session_id=session_id, user_id=user["user_id"])
        return ChatResponse(**response_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error sending chat message", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to send message")

@router.get("/chat/sessions/{session_id}/messages", response_model=List[ChatMessageResponse])
async def get_chat_messages(
    session_id: str,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Get messages for a chat session"""
    try:
        chat_service = get_chat_service()

        # Get session info to extract workbench_id
        session_result = supabase.client.table("session").select("*").eq("session_id", session_id).execute()

        if not session_result.data:
            raise HTTPException(status_code=404, detail="Chat session not found")

        session_data = session_result.data[0]
        workbench_id = session_data["workbench_id"]

        messages = await chat_service.get_session_messages(
            session_id=session_id,
            user_id=user["user_id"],
            workbench_id=workbench_id
        )

        return [ChatMessageResponse(**msg) for msg in messages]

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting chat messages", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get messages")

@router.get("/chat/sessions")
async def list_chat_sessions(
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """List chat sessions for the current user"""
    try:
        result = supabase.client.table("session").select("*").eq("user_id", user["user_id"]).order("created_at", desc=True).execute()

        sessions = []
        for session in result.data:
            sessions.append({
                "session_id": session["session_id"],
                "title": session["title"],
                "workbench_id": session["workbench_id"],
                "created_at": session["created_at"]
            })

        return sessions

    except Exception as e:
        logger.error("Error listing chat sessions", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to list sessions")
