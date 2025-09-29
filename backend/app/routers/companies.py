from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
import structlog
from ..deps import get_supabase_client, get_user_info
from ..models.company import (
    CompanyCreate,
    CompanyResponse,
    CompanyMemberCreate,
    CompanyMemberResponse,
    CompanyUpdate
)

logger = structlog.get_logger()
router = APIRouter()

async def verify_company_access(
    company_id: str,
    user: dict,
    supabase,
    required_role: Optional[str] = None
) -> dict:
    """Verify user has access to company and return company data"""
    result = supabase.client.table("company").select("*").eq("company_id", company_id).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Company not found")

    company = result.data[0]

    # Check if user is a member of the company
    member_result = supabase.client.table("company_members").select("*").eq("company_id", company_id).eq("user_id", user["user_id"]).execute()

    if not member_result.data:
        raise HTTPException(status_code=403, detail="Access denied to company")

    member = member_result.data[0]

    if required_role and member["role"] not in ["admin", required_role]:
        raise HTTPException(status_code=403, detail=f"Insufficient permissions. Required: {required_role}")

    return company

@router.post("/companies", response_model=CompanyResponse)
async def create_company(
    company: CompanyCreate,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Create a new company"""
    try:
        # Insert company
        result = supabase.client.table("company").insert({
            "name": company.name,
            "description": company.description,
            "domain": company.domain
        }).execute()

        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to create company")

        company_data = result.data[0]
        company_id = company_data["company_id"]

        # Add creator as admin member
        member_result = supabase.client.table("company_members").insert({
            "company_id": company_id,
            "user_id": user["user_id"],
            "role": "admin"
        }).execute()

        if not member_result.data:
            logger.warning("Failed to add company creator as admin member", company_id=company_id, user_id=user["user_id"])

        logger.info("Created company", company_id=company_id, user_id=user["user_id"])
        return CompanyResponse(**company_data)

    except Exception as e:
        logger.error("Error creating company", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to create company")

@router.get("/companies", response_model=List[CompanyResponse])
async def list_companies(
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """List companies the user is a member of"""
    try:
        # Get companies where user is a member (filtered by RLS)
        result = supabase.client.table("company").select("*").execute()
        return [CompanyResponse(**item) for item in result.data]

    except Exception as e:
        logger.error("Error listing companies", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to list companies")

@router.get("/companies/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: str,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Get a specific company"""
    try:
        await verify_company_access(company_id, user, supabase)
        result = supabase.client.table("company").select("*").eq("company_id", company_id).execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Company not found")

        return CompanyResponse(**result.data[0])

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting company", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get company")

@router.patch("/companies/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: str,
    company_update: CompanyUpdate,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Update company details (admin only)"""
    try:
        # Verify user is admin
        await verify_company_access(company_id, user, supabase, "admin")

        # Build update data
        update_data = {}
        if company_update.name is not None:
            update_data["name"] = company_update.name
        if company_update.description is not None:
            update_data["description"] = company_update.description
        if company_update.domain is not None:
            update_data["domain"] = company_update.domain

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        result = supabase.client.table("company").update(update_data).eq("company_id", company_id).execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Company not found")

        logger.info("Updated company", company_id=company_id, user_id=user["user_id"])
        return CompanyResponse(**result.data[0])

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error updating company", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to update company")

@router.post("/companies/{company_id}/members", response_model=CompanyMemberResponse)
async def add_company_member(
    company_id: str,
    member: CompanyMemberCreate,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Add a member to a company (admin only)"""
    try:
        # Verify user is admin
        await verify_company_access(company_id, user, supabase, "admin")

        # Check if member already exists
        existing = supabase.client.table("company_members").select("*").eq("company_id", company_id).eq("user_id", member.user_id).execute()

        if existing.data:
            raise HTTPException(status_code=400, detail="User is already a member of this company")

        # Add member
        result = supabase.client.table("company_members").insert({
            "company_id": company_id,
            "user_id": member.user_id,
            "role": member.role
        }).execute()

        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to add member")

        logger.info("Added company member", company_id=company_id, user_id=member.user_id, role=member.role)
        return CompanyMemberResponse(**result.data[0])

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error adding company member", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to add member")

@router.get("/companies/{company_id}/members", response_model=List[CompanyMemberResponse])
async def list_company_members(
    company_id: str,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """List members of a company"""
    try:
        # Verify access
        await verify_company_access(company_id, user, supabase)

        result = supabase.client.table("company_members").select("*").eq("company_id", company_id).execute()
        return [CompanyMemberResponse(**item) for item in result.data]

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error listing company members", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to list members")

@router.put("/companies/{company_id}/members/{member_user_id}")
async def update_company_member_role(
    company_id: str,
    member_user_id: str,
    role: str,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Update company member role (admin only)"""
    try:
        # Verify user is admin
        await verify_company_access(company_id, user, supabase, "admin")

        if role not in ["admin", "member", "viewer"]:
            raise HTTPException(status_code=400, detail="Invalid role")

        result = supabase.client.table("company_members").update({"role": role}).eq("company_id", company_id).eq("user_id", member_user_id).execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Member not found")

        logger.info("Updated company member role", company_id=company_id, user_id=member_user_id, role=role)
        return {"message": "Member role updated successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error updating company member role", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to update member role")

@router.delete("/companies/{company_id}/members/{member_user_id}")
async def remove_company_member(
    company_id: str,
    member_user_id: str,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Remove a member from a company (admin only)"""
    try:
        # Verify user is admin
        await verify_company_access(company_id, user, supabase, "admin")

        # Prevent removing the last admin
        admin_count_result = supabase.client.table("company_members").select("id").eq("company_id", company_id).eq("role", "admin").execute()

        if len(admin_count_result.data) <= 1:
            admin_member_result = supabase.client.table("company_members").select("*").eq("company_id", company_id).eq("user_id", member_user_id).execute()
            if admin_member_result.data and admin_member_result.data[0]["role"] == "admin":
                raise HTTPException(status_code=400, detail="Cannot remove the last admin from company")

        result = supabase.client.table("company_members").delete().eq("company_id", company_id).eq("user_id", member_user_id).execute()

        logger.info("Removed company member", company_id=company_id, user_id=member_user_id)
        return {"message": "Member removed successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error removing company member", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to remove member")
