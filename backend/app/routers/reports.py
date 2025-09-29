from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import structlog
from ..deps import get_supabase_client, get_user_info
from ..services.report_service import get_report_service
from ..models.report import (
    ReportGenerateRequest,
    ReportResponse,
    CompanyReportGenerateRequest,
    CompanyReportResponse
)

logger = structlog.get_logger()
router = APIRouter()

@router.post("/reports/workbench", response_model=ReportResponse)
async def generate_workbench_report(
    request: ReportGenerateRequest,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Generate a report for a workbench"""
    try:
        report_service = get_report_service()

        report_data = await report_service.generate_workbench_report(
            workbench_id=request.workbench_id,
            user_id=user["user_id"],
            report_type=request.report_type
        )

        logger.info("Generated workbench report", report_id=report_data["report_id"], user_id=user["user_id"])
        return ReportResponse(**report_data)

    except Exception as e:
        logger.error("Error generating workbench report", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate report")

@router.post("/reports/company", response_model=CompanyReportResponse)
async def generate_company_report(
    request: CompanyReportGenerateRequest,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Generate a report for a company"""
    try:
        report_service = get_report_service()

        report_data = await report_service.generate_company_report(
            company_id=request.company_id,
            user_id=user["user_id"],
            report_type=request.report_type
        )

        logger.info("Generated company report", report_id=report_data["report_id"], user_id=user["user_id"])
        return CompanyReportResponse(**report_data)

    except Exception as e:
        logger.error("Error generating company report", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate report")

@router.get("/reports/workbench")
async def list_workbench_reports(
    workbench_id: str,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """List reports for a workbench"""
    try:
        # Verify access to workbench
        report_service = get_report_service()
        await report_service._verify_workbench_access(workbench_id, user["user_id"])

        result = supabase.client.table("report").select("*").eq("workbench_id", workbench_id).eq("user_id", user["user_id"]).order("generated_at", desc=True).execute()

        reports = []
        for report in result.data:
            reports.append({
                "report_id": report["report_id"],
                "workbench_id": report["workbench_id"],
                "user_id": report["user_id"],
                "report_type": report["report_type"],
                "generated_at": report["generated_at"]
            })

        return reports

    except Exception as e:
        logger.error("Error listing workbench reports", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to list reports")

@router.get("/reports/company")
async def list_company_reports(
    company_id: str,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """List reports for a company"""
    try:
        # Verify access to company
        report_service = get_report_service()
        await report_service._verify_company_access(company_id, user["user_id"])

        result = supabase.client.table("company_report").select("*").eq("company_id", company_id).eq("user_id", user["user_id"]).order("generated_at", desc=True).execute()

        reports = []
        for report in result.data:
            reports.append({
                "report_id": report["report_id"],
                "company_id": report["company_id"],
                "user_id": report["user_id"],
                "report_type": report["report_type"],
                "generated_at": report["generated_at"]
            })

        return reports

    except Exception as e:
        logger.error("Error listing company reports", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to list reports")

@router.get("/reports/workbench/{report_id}")
async def get_workbench_report(
    report_id: str,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Get a specific workbench report"""
    try:
        result = supabase.client.table("report").select("*").eq("report_id", report_id).eq("user_id", user["user_id"]).execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Report not found")

        report = result.data[0]
        return {
            "report_id": report["report_id"],
            "workbench_id": report["workbench_id"],
            "user_id": report["user_id"],
            "report_type": report["report_type"],
            "content": report["content"],
            "generated_at": report["generated_at"]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting workbench report", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get report")

@router.get("/reports/company/{report_id}")
async def get_company_report(
    report_id: str,
    user: dict = Depends(get_user_info),
    supabase = Depends(get_supabase_client)
):
    """Get a specific company report"""
    try:
        result = supabase.client.table("company_report").select("*").eq("report_id", report_id).eq("user_id", user["user_id"]).execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Report not found")

        report = result.data[0]
        return {
            "report_id": report["report_id"],
            "company_id": report["company_id"],
            "user_id": report["user_id"],
            "report_type": report["report_type"],
            "content": report["content"],
            "generated_at": report["generated_at"]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting company report", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get report")
