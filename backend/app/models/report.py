from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ReportFormat(str, Enum):
    PDF = "pdf"
    EXCEL = "excel"
    WORD = "word"
    HTML = "html"
    JSON = "json"

class ReportTemplate(str, Enum):
    FINANCIAL_SUMMARY = "financial_summary"
    BUSINESS_ANALYSIS = "business_analysis"
    PERFORMANCE_DASHBOARD = "performance_dashboard"
    EXECUTIVE_SUMMARY = "executive_summary"
    DETAILED_FINANCIAL = "detailed_financial"
    TREND_ANALYSIS = "trend_analysis"
    RISK_ASSESSMENT = "risk_assessment"
    STRATEGIC_PLAN = "strategic_plan"

class ReportTemplateDefinition(BaseModel):
    template_id: str
    name: str
    description: str
    output_format: ReportFormat
    sections: List[Dict[str, Any]]
    styling: Optional[Dict[str, Any]] = None

class ReportGenerateRequest(BaseModel):
    workbench_id: str = Field(..., description="ID of the workbench to generate report for")
    template_id: str = Field(..., description="Template to use for report generation")
    output_format: ReportFormat = Field(ReportFormat.PDF, description="Output format")
    include_charts: bool = Field(True, description="Include charts and visualizations")
    custom_parameters: Optional[Dict[str, Any]] = None

class ReportResponse(BaseModel):
    report_id: str
    template_id: str
    output_format: ReportFormat
    download_url: Optional[str]
    content: str
    metadata: Dict[str, Any]
    generated_at: datetime
