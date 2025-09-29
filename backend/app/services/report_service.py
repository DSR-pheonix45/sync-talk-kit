from typing import Dict, Any, Optional, List
import structlog
from datetime import datetime
from ..services.supabase_client import supabase_client
from ..services.chat_service import get_chat_service
from ..core.config import settings

logger = structlog.get_logger()

class ReportService:
    """Report generation service with templates and data analysis"""

    def __init__(self):
        self.supabase = supabase_client
        self.chat_service = get_chat_service()

    async def generate_workbench_report(
        self,
        workbench_id: str,
        user_id: str,
        report_type: str = "summary"
    ) -> Dict[str, Any]:
        """Generate a comprehensive report for a workbench"""
        try:
            # Verify access to workbench
            await self._verify_workbench_access(workbench_id, user_id)

            # Gather all data for the report
            workbench_data = await self._get_workbench_data(workbench_id)
            files_data = await self._get_files_data(workbench_id)
            members_data = await self._get_members_data(workbench_id)
            chunks_data = await self._get_chunks_data(workbench_id)
            sessions_data = await self._get_sessions_data(user_id, workbench_id)

            # Generate report based on type
            if report_type == "summary":
                report_content = await self._generate_summary_report(
                    workbench_data, files_data, members_data, chunks_data, sessions_data
                )
            elif report_type == "detailed":
                report_content = await self._generate_detailed_report(
                    workbench_data, files_data, members_data, chunks_data, sessions_data
                )
            elif report_type == "analysis":
                report_content = await self._generate_analysis_report(
                    workbench_data, files_data, chunks_data, sessions_data
                )
            else:
                raise ValueError(f"Unknown report type: {report_type}")

            # Create report record
            report_id = await self._store_report(
                workbench_id, user_id, report_type, report_content
            )

            logger.info("Generated workbench report", report_id=report_id, workbench_id=workbench_id, report_type=report_type)
            return {
                "report_id": report_id,
                "report_type": report_type,
                "content": report_content,
                "generated_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error("Error generating workbench report", error=str(e))
            raise

    async def generate_company_report(
        self,
        company_id: str,
        user_id: str,
        report_type: str = "summary"
    ) -> Dict[str, Any]:
        """Generate a comprehensive report for a company"""
        try:
            # Verify access to company
            await self._verify_company_access(company_id, user_id)

            # Gather company data
            company_data = await self._get_company_data(company_id)
            workbenches_data = await self._get_company_workbenches(company_id)
            members_data = await self._get_company_members(company_id)

            # Generate report
            if report_type == "summary":
                report_content = await self._generate_company_summary_report(
                    company_data, workbenches_data, members_data
                )
            elif report_type == "activity":
                report_content = await self._generate_company_activity_report(
                    company_data, workbenches_data, members_data
                )
            else:
                raise ValueError(f"Unknown company report type: {report_type}")

            # Create report record
            report_id = await self._store_company_report(
                company_id, user_id, report_type, report_content
            )

            logger.info("Generated company report", report_id=report_id, company_id=company_id, report_type=report_type)
            return {
                "report_id": report_id,
                "report_type": report_type,
                "content": report_content,
                "generated_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error("Error generating company report", error=str(e))
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

    async def _verify_company_access(self, company_id: str, user_id: str):
        """Verify user has access to company"""
        result = self.supabase.client.table("company").select("*").eq("company_id", company_id).execute()

        if not result.data:
            raise Exception("Company not found")

        # Check if user is a member
        member_result = self.supabase.client.table("company_members").select("*").eq("company_id", company_id).eq("user_id", user_id).execute()

        if not member_result.data:
            raise Exception("Access denied to company")

    async def _get_workbench_data(self, workbench_id: str) -> Dict[str, Any]:
        """Get workbench information"""
        result = self.supabase.client.table("workbench").select("*").eq("id", workbench_id).execute()
        return result.data[0] if result.data else {}

    async def _get_files_data(self, workbench_id: str) -> List[Dict[str, Any]]:
        """Get workbench files information"""
        result = self.supabase.client.table("workbench_files").select("*").eq("workbench_id", workbench_id).execute()
        return result.data if result.data else []

    async def _get_members_data(self, workbench_id: str) -> List[Dict[str, Any]]:
        """Get workbench members information"""
        result = self.supabase.client.table("workbench_members").select("*").eq("workbench_id", workbench_id).execute()
        return result.data if result.data else []

    async def _get_chunks_data(self, workbench_id: str) -> List[Dict[str, Any]]:
        """Get workbench chunks information"""
        result = self.supabase.client.table("workbench_chunks").select("*").eq("workbench_id", workbench_id).execute()
        return result.data if result.data else []

    async def _get_sessions_data(self, user_id: str, workbench_id: str) -> List[Dict[str, Any]]:
        """Get chat sessions for workbench"""
        result = self.supabase.client.table("session").select("*").eq("user_id", user_id).eq("workbench_id", workbench_id).execute()
        return result.data if result.data else []

    async def _get_company_data(self, company_id: str) -> Dict[str, Any]:
        """Get company information"""
        result = self.supabase.client.table("company").select("*").eq("company_id", company_id).execute()
        return result.data[0] if result.data else {}

    async def _get_company_workbenches(self, company_id: str) -> List[Dict[str, Any]]:
        """Get all workbenches for a company"""
        result = self.supabase.client.table("workbench").select("*").eq("company_id", company_id).execute()
        return result.data if result.data else []

    async def _get_company_members(self, company_id: str) -> List[Dict[str, Any]]:
        """Get company members information"""
        result = self.supabase.client.table("company_members").select("*").eq("company_id", company_id).execute()
        return result.data if result.data else []

    async def _generate_summary_report(
        self,
        workbench: Dict,
        files: List[Dict],
        members: List[Dict],
        chunks: List[Dict],
        sessions: List[Dict]
    ) -> str:
        """Generate summary report"""
        return f"""
# Workbench Summary Report

## Overview
- **Name**: {workbench.get('name', 'N/A')}
- **Description**: {workbench.get('description', 'N/A')}
- **Created**: {workbench.get('created_at', 'N/A')}

## Files
- **Total Files**: {len(files)}
- **Indexed Files**: {sum(1 for f in files if f.get('status') == 'indexed')}
- **Pending Files**: {sum(1 for f in files if f.get('status') == 'pending')}
- **Failed Files**: {sum(1 for f in files if f.get('status') == 'error')}

## Team
- **Total Members**: {len(members)}
- **Owners**: {sum(1 for m in members if m.get('role') == 'owner')}
- **Editors**: {sum(1 for m in members if m.get('role') == 'editor')}
- **Viewers**: {sum(1 for m in members if m.get('role') == 'viewer')}

## Content
- **Total Chunks**: {len(chunks)}
- **Chat Sessions**: {len(sessions)}

## Recent Activity
Files uploaded and processed for analysis.
"""

    async def _generate_detailed_report(
        self,
        workbench: Dict,
        files: List[Dict],
        members: List[Dict],
        chunks: List[Dict],
        sessions: List[Dict]
    ) -> str:
        """Generate detailed report"""
        # Implementation for detailed report
        return await self._generate_summary_report(workbench, files, members, chunks, sessions)

    async def _generate_analysis_report(
        self,
        workbench: Dict,
        files: List[Dict],
        chunks: List[Dict],
        sessions: List[Dict]
    ) -> str:
        """Generate analysis report with insights"""
        # Implementation for analysis report
        return await self._generate_summary_report(workbench, files, [], chunks, sessions)

    async def _generate_company_summary_report(
        self,
        company: Dict,
        workbenches: List[Dict],
        members: List[Dict]
    ) -> str:
        """Generate company summary report"""
        return f"""
# Company Summary Report

## Overview
- **Name**: {company.get('name', 'N/A')}
- **Description**: {company.get('description', 'N/A')}
- **Domain**: {company.get('domain', 'N/A')}

## Workbenches
- **Total Workbenches**: {len(workbenches)}
- **Active Workbenches**: {sum(1 for w in workbenches if w.get('created_at'))}

## Team
- **Total Members**: {len(members)}
- **Admins**: {sum(1 for m in members if m.get('role') == 'admin')}
- **Members**: {sum(1 for m in members if m.get('role') == 'member')}
- **Viewers**: {sum(1 for m in members if m.get('role') == 'viewer')}

## Activity Summary
Company collaboration and document management platform.
"""

    async def _generate_company_activity_report(
        self,
        company: Dict,
        workbenches: List[Dict],
        members: List[Dict]
    ) -> str:
        """Generate company activity report"""
        return await self._generate_company_summary_report(company, workbenches, members)

    async def _store_report(
        self,
        workbench_id: str,
        user_id: str,
        report_type: str,
        content: str
    ) -> str:
        """Store generated report"""
        try:
            report_data = {
                "workbench_id": workbench_id,
                "user_id": user_id,
                "report_type": report_type,
                "content": content,
                "generated_at": datetime.utcnow().isoformat()
            }

            result = self.supabase.client.table("report").insert(report_data).execute()

            if not result.data:
                raise Exception("Failed to store report")

            return result.data[0]["report_id"]

        except Exception as e:
            logger.error("Error storing report", error=str(e))
            raise

    async def _store_company_report(
        self,
        company_id: str,
        user_id: str,
        report_type: str,
        content: str
    ) -> str:
        """Store generated company report"""
        try:
            report_data = {
                "company_id": company_id,
                "user_id": user_id,
                "report_type": report_type,
                "content": content,
                "generated_at": datetime.utcnow().isoformat()
            }

            result = self.supabase.client.table("company_report").insert(report_data).execute()

            if not result.data:
                raise Exception("Failed to store company report")

            return result.data[0]["report_id"]

        except Exception as e:
            logger.error("Error storing company report", error=str(e))
            raise

# Global report service instance
report_service: Optional[ReportService] = None

def get_report_service() -> ReportService:
    """Get or create report service instance"""
    global report_service
    if report_service is None:
        report_service = ReportService()
    return report_service
