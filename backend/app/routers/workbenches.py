from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from typing import List, Optional
import structlog
from ..services.storage_service import get_storage_service
from ..models.workbench import (
    WorkbenchCreate,
    WorkbenchResponse,
    WorkbenchMemberCreate,
    WorkbenchMemberResponse,
    WorkbenchFileCreate,
    WorkbenchFileResponse,
    WorkbenchFileStatus
)

logger = structlog.get_logger()
router = APIRouter()

async def verify_workbench_access(
    workbench_id: str,
    user: dict,
    supabase,
    required_role: Optional[str] = None
) -> dict:
    """Verify user has access to workbench and return workbench data"""
    result = supabase.client.table("workbench").select("*").eq("id", workbench_id).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Workbench not found")

    workbench = result.data[0]

    # Check if user is owner
    if workbench["owner_user_id"] == user["user_id"]:
        return workbench

    # Check if user is a member with appropriate role
    member_result = supabase.client.table("workbench_members").select("*").eq("workbench_id", workbench_id).eq("user_id", user["user_id"]).execute()

    if not member_result.data:
        raise HTTPException(status_code=403, detail="Access denied to workbench")

    member = member_result.data[0]

    if required_role and member["role"] not in ["owner", required_role]:
        raise HTTPException(status_code=403, detail=f"Insufficient permissions. Required: {required_role}")

    return workbench

@router.post("/workbenches", response_model=WorkbenchResponse)
async def create_workbench(
    workbench: WorkbenchCreate,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Create a new workbench"""
    try:
        # Insert workbench
        result = supabase.client.table("workbench").insert({
            "name": workbench.name,
            "description": workbench.description,
            "owner_user_id": user["user_id"],
            "company_id": workbench.company_id
        }).execute()

        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to create workbench")

        workbench_data = result.data[0]
        logger.info("Created workbench", workbench_id=workbench_data["id"], user_id=user["user_id"])

        return WorkbenchResponse(**workbench_data)

    except Exception as e:
        logger.error("Error creating workbench", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to create workbench")

@router.get("/workbenches", response_model=List[WorkbenchResponse])
async def list_workbenches(
    company_id: Optional[str] = Query(None, description="Filter by company ID"),
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """List workbenches accessible to the user"""
    try:
        query = supabase.client.table("workbench").select("*")

        if company_id:
            query = query.eq("company_id", company_id)

        result = query.execute()
        return [WorkbenchResponse(**item) for item in result.data]

    except Exception as e:
        logger.error("Error listing workbenches", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to list workbenches")

@router.get("/workbenches/{workbench_id}", response_model=WorkbenchResponse)
async def get_workbench(
    workbench_id: str,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Get a specific workbench"""
    try:
        await verify_workbench_access(workbench_id, user, supabase)
        result = supabase.client.table("workbench").select("*").eq("id", workbench_id).execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Workbench not found")

        return WorkbenchResponse(**result.data[0])

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting workbench", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get workbench")

@router.post("/workbenches/{workbench_id}/members", response_model=WorkbenchMemberResponse)
async def add_workbench_member(
    workbench_id: str,
    member: WorkbenchMemberCreate,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Add a member to a workbench (owners only)"""
    try:
        # Verify user is owner
        await verify_workbench_access(workbench_id, user, supabase, "owner")

        # Check if member already exists
        existing = supabase.client.table("workbench_members").select("*").eq("workbench_id", workbench_id).eq("user_id", member.user_id).execute()

        if existing.data:
            raise HTTPException(status_code=400, detail="User is already a member of this workbench")

        # Add member
        result = supabase.client.table("workbench_members").insert({
            "workbench_id": workbench_id,
            "user_id": member.user_id,
            "role": member.role
        }).execute()

        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to add member")

        logger.info("Added workbench member", workbench_id=workbench_id, user_id=member.user_id, role=member.role)
        return WorkbenchMemberResponse(**result.data[0])

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error adding workbench member", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to add member")

@router.get("/workbenches/{workbench_id}/members", response_model=List[WorkbenchMemberResponse])
async def list_workbench_members(
    workbench_id: str,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """List members of a workbench"""
    try:
        # Verify access
        await verify_workbench_access(workbench_id, user, supabase)

        result = supabase.client.table("workbench_members").select("*").eq("workbench_id", workbench_id).execute()
        return [WorkbenchMemberResponse(**item) for item in result.data]

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error listing workbench members", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to list members")

@router.put("/workbenches/{workbench_id}/members/{member_user_id}")
async def update_member_role(
    workbench_id: str,
    member_user_id: str,
    role: str,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Update member role (owners only)"""
    try:
        # Verify user is owner
        await verify_workbench_access(workbench_id, user, supabase, "owner")

        if role not in ["owner", "editor", "viewer"]:
            raise HTTPException(status_code=400, detail="Invalid role")

        result = supabase.client.table("workbench_members").update({"role": role}).eq("workbench_id", workbench_id).eq("user_id", member_user_id).execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Member not found")

        logger.info("Updated member role", workbench_id=workbench_id, user_id=member_user_id, role=role)
        return {"message": "Member role updated successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error updating member role", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to update member role")

@router.delete("/workbenches/{workbench_id}/members/{member_user_id}")
async def remove_workbench_member(
    workbench_id: str,
    member_user_id: str,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Remove a member from a workbench (owners only)"""
    try:
        # Verify user is owner
        await verify_workbench_access(workbench_id, user, supabase, "owner")

        result = supabase.client.table("workbench_members").delete().eq("workbench_id", workbench_id).eq("user_id", member_user_id).execute()

        logger.info("Removed workbench member", workbench_id=workbench_id, user_id=member_user_id)
        return {"message": "Member removed successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error removing workbench member", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to remove member")

@router.post("/workbenches/{workbench_id}/files", response_model=WorkbenchFileResponse)
async def upload_file(
    workbench_id: str,
    file: UploadFile = File(...),
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Upload a file to a workbench"""
    try:
        # Verify user has editor or owner access
        await verify_workbench_access(workbench_id, user, supabase, "editor")

        # Read file content
        file_content = await file.read()
        file_size = len(file_content)

        # Get storage service
        storage = get_storage_service()

        # Upload to Supabase Storage
        storage_filename = await storage.upload_file(
            file.filename,
            file_content,
            file.content_type or "application/octet-stream"
        )

        if not storage_filename:
            raise HTTPException(status_code=500, detail="Failed to upload file to storage")

        # Create file record in database
        file_data = {
            "workbench_id": workbench_id,
            "storage_file_id": storage_filename,
            "file_name": file.filename,
            "file_type": file.content_type,
            "size_bytes": file_size,
            "status": "pending"
        }

        result = supabase.client.table("workbench_files").insert(file_data).execute()

        if not result.data:
            # Clean up uploaded file if database insert fails
            await storage.delete_file(storage_filename)
            raise HTTPException(status_code=500, detail="Failed to create file record")

        file_record = result.data[0]

        # Trigger background indexing
        try:
            from ..workers.indexing import get_indexing_worker
            worker = get_indexing_worker()
            # Run indexing in background (fire and forget)
            asyncio.create_task(worker.process_file(file_record["id"], workbench_id))
        except Exception as e:
            logger.warning("Failed to trigger indexing", file_id=file_record["id"], error=str(e))

        logger.info("Uploaded file", file_id=file_record["id"], workbench_id=workbench_id, filename=file.filename)
        return WorkbenchFileResponse(**file_record)

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error uploading file", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to upload file")

@router.get("/workbenches/{workbench_id}/files", response_model=List[WorkbenchFileResponse])
async def list_files(
    workbench_id: str,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """List files in a workbench"""
    try:
        # Verify access
        await verify_workbench_access(workbench_id, user, supabase)

        result = supabase.client.table("workbench_files").select("*").eq("workbench_id", workbench_id).execute()
        return [WorkbenchFileResponse(**item) for item in result.data]

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error listing files", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to list files")

@router.get("/workbenches/{workbench_id}/files/{file_id}/download")
async def download_file(
    workbench_id: str,
    file_id: str,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Download a file from a workbench"""
    try:
        # Verify access
        await verify_workbench_access(workbench_id, user, supabase)

        # Get file info
        file_result = supabase.client.table("workbench_files").select("*").eq("id", file_id).eq("workbench_id", workbench_id).execute()

        if not file_result.data:
            raise HTTPException(status_code=404, detail="File not found")

        file_info = file_result.data[0]
        storage_file_id = file_info["storage_file_id"]

        if not storage_file_id:
            raise HTTPException(status_code=404, detail="File not found in storage")

        # Get download URL from storage
        from ..core.config import settings
        bucket_name = settings.supabase_storage_bucket

        download_url = supabase.client.storage.from_(bucket_name).get_public_url(storage_file_id)

        return {"download_url": download_url}

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error downloading file", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to download file")

@router.get("/workbenches/{workbench_id}/status")
async def get_workbench_status(
    workbench_id: str,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Get workbench indexing status and any errors"""
    try:
        # Verify access
        await verify_workbench_access(workbench_id, user, supabase)

        # Get file status summary
        files_result = supabase.client.table("workbench_files").select("status, error_message").eq("workbench_id", workbench_id).execute()

        if not files_result.data:
            return {
                "status": "empty",
                "total_files": 0,
                "indexed_files": 0,
                "failed_files": 0,
                "errors": []
            }

        files = files_result.data
        total_files = len(files)
        indexed_files = sum(1 for f in files if f["status"] == "indexed")
        failed_files = sum(1 for f in files if f["status"] == "error")
        errors = [f["error_message"] for f in files if f["error_message"]]

        status = "ready" if indexed_files == total_files else "processing" if indexed_files > 0 else "error"

        return {
            "status": status,
            "total_files": total_files,
            "indexed_files": indexed_files,
            "failed_files": failed_files,
            "errors": errors
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting workbench status", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get workbench status")
