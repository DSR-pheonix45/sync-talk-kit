from typing import Dict, Any, List
from .models.report import ReportTemplate, ReportFormat, ReportTemplateDefinition

# Report Templates Configuration
REPORT_TEMPLATES = {
    ReportTemplate.FINANCIAL_SUMMARY: ReportTemplateDefinition(
        template_id=ReportTemplate.FINANCIAL_SUMMARY,
        name="Financial Summary Report",
        description="Comprehensive financial overview with key metrics and trends",
        output_format=ReportFormat.PDF,
        sections=[
            {
                "id": "executive_summary",
                "title": "Executive Summary",
                "type": "text",
                "content_template": "Financial performance summary for {period}"
            },
            {
                "id": "key_metrics",
                "title": "Key Financial Metrics",
                "type": "table",
                "columns": ["Metric", "Current Period", "Previous Period", "Change %"],
                "data_source": "financial_metrics"
            },
            {
                "id": "revenue_analysis",
                "title": "Revenue Analysis",
                "type": "chart",
                "chart_type": "line",
                "data_source": "revenue_trends"
            },
            {
                "id": "expense_breakdown",
                "title": "Expense Breakdown",
                "type": "chart",
                "chart_type": "pie",
                "data_source": "expense_categories"
            },
            {
                "id": "profitability",
                "title": "Profitability Analysis",
                "type": "text",
                "content_template": "Analysis of profit margins and profitability trends"
            }
        ]
    ),

    ReportTemplate.BUSINESS_ANALYSIS: ReportTemplateDefinition(
        template_id=ReportTemplate.BUSINESS_ANALYSIS,
        name="Business Analysis Report",
        description="Detailed business performance analysis with insights",
        output_format=ReportFormat.PDF,
        sections=[
            {
                "id": "business_overview",
                "title": "Business Overview",
                "type": "text",
                "content_template": "Current business status and key achievements"
            },
            {
                "id": "market_analysis",
                "title": "Market Analysis",
                "type": "text",
                "content_template": "Market position and competitive landscape"
            },
            {
                "id": "performance_metrics",
                "title": "Performance Metrics",
                "type": "table",
                "columns": ["KPI", "Target", "Actual", "Variance"],
                "data_source": "kpi_data"
            },
            {
                "id": "swot_analysis",
                "title": "SWOT Analysis",
                "type": "text",
                "content_template": "Strengths, Weaknesses, Opportunities, Threats analysis"
            }
        ]
    ),

    ReportTemplate.EXECUTIVE_SUMMARY: ReportTemplateDefinition(
        template_id=ReportTemplate.EXECUTIVE_SUMMARY,
        name="Executive Summary",
        description="High-level executive summary for leadership",
        output_format=ReportFormat.PDF,
        sections=[
            {
                "id": "key_highlights",
                "title": "Key Highlights",
                "type": "text",
                "content_template": "Major achievements and milestones"
            },
            {
                "id": "financial_snapshot",
                "title": "Financial Snapshot",
                "type": "table",
                "columns": ["Metric", "Value", "Status"],
                "data_source": "executive_metrics"
            },
            {
                "id": "strategic_priorities",
                "title": "Strategic Priorities",
                "type": "text",
                "content_template": "Current strategic focus areas and priorities"
            }
        ]
    ),

    ReportTemplate.DETAILED_FINANCIAL: ReportTemplateDefinition(
        template_id=ReportTemplate.DETAILED_FINANCIAL,
        name="Detailed Financial Report",
        description="Comprehensive financial analysis with detailed breakdowns",
        output_format=ReportFormat.EXCEL,
        sections=[
            {
                "id": "income_statement",
                "title": "Income Statement",
                "type": "table",
                "columns": ["Line Item", "Current Year", "Previous Year", "Variance"],
                "data_source": "income_statement"
            },
            {
                "id": "balance_sheet",
                "title": "Balance Sheet",
                "type": "table",
                "columns": ["Asset/Liability", "Current Period", "Previous Period"],
                "data_source": "balance_sheet"
            },
            {
                "id": "cash_flow",
                "title": "Cash Flow Statement",
                "type": "table",
                "columns": ["Cash Flow Category", "Amount", "Notes"],
                "data_source": "cash_flow"
            }
        ]
    ),

    ReportTemplate.TREND_ANALYSIS: ReportTemplateDefinition(
        template_id=ReportTemplate.TREND_ANALYSIS,
        name="Trend Analysis Report",
        description="Analysis of trends and patterns in business data",
        output_format=ReportFormat.PDF,
        sections=[
            {
                "id": "trend_overview",
                "title": "Trend Overview",
                "type": "text",
                "content_template": "Summary of identified trends and patterns"
            },
            {
                "id": "revenue_trends",
                "title": "Revenue Trends",
                "type": "chart",
                "chart_type": "line",
                "data_source": "revenue_trends"
            },
            {
                "id": "growth_analysis",
                "title": "Growth Analysis",
                "type": "text",
                "content_template": "Analysis of growth patterns and projections"
            }
        ]
    ),

    ReportTemplate.RISK_ASSESSMENT: ReportTemplateDefinition(
        template_id=ReportTemplate.RISK_ASSESSMENT,
        name="Risk Assessment Report",
        description="Comprehensive risk analysis and mitigation strategies",
        output_format=ReportFormat.PDF,
        sections=[
            {
                "id": "risk_summary",
                "title": "Risk Summary",
                "type": "text",
                "content_template": "Overview of identified risks and their potential impact"
            },
            {
                "id": "risk_matrix",
                "title": "Risk Matrix",
                "type": "table",
                "columns": ["Risk Category", "Likelihood", "Impact", "Mitigation"],
                "data_source": "risk_data"
            },
            {
                "id": "mitigation_strategies",
                "title": "Mitigation Strategies",
                "type": "text",
                "content_template": "Detailed mitigation plans and recommendations"
            }
        ]
    ),

    ReportTemplate.STRATEGIC_PLAN: ReportTemplateDefinition(
        template_id=ReportTemplate.STRATEGIC_PLAN,
        name="Strategic Plan",
        description="Strategic planning document with goals and objectives",
        output_format=ReportFormat.WORD,
        sections=[
            {
                "id": "strategic_overview",
                "title": "Strategic Overview",
                "type": "text",
                "content_template": "Strategic direction and planning framework"
            },
            {
                "id": "goals_objectives",
                "title": "Goals and Objectives",
                "type": "table",
                "columns": ["Objective", "Timeline", "Success Metrics", "Owner"],
                "data_source": "strategic_goals"
            },
            {
                "id": "action_plan",
                "title": "Action Plan",
                "type": "text",
                "content_template": "Detailed action plan with timelines and responsibilities"
            }
        ]
    ),

    ReportTemplate.PERFORMANCE_DASHBOARD: ReportTemplateDefinition(
        template_id=ReportTemplate.PERFORMANCE_DASHBOARD,
        name="Performance Dashboard",
        description="Visual dashboard with key performance indicators",
        output_format=ReportFormat.HTML,
        sections=[
            {
                "id": "dashboard_overview",
                "title": "Performance Dashboard",
                "type": "dashboard",
                "widgets": [
                    {"type": "kpi_card", "title": "Revenue", "data_source": "revenue_kpi"},
                    {"type": "kpi_card", "title": "Profit Margin", "data_source": "margin_kpi"},
                    {"type": "chart", "title": "Monthly Trends", "chart_type": "line"},
                    {"type": "table", "title": "Top Products", "data_source": "top_products"}
                ]
            }
        ]
    )
}

def get_template(template_id: str) -> Optional[ReportTemplateDefinition]:
    """Get a report template by ID"""
    return REPORT_TEMPLATES.get(ReportTemplate(template_id))

def get_available_templates() -> List[Dict[str, Any]]:
    """Get all available report templates"""
    return [
        {
            "template_id": template.template_id,
            "name": template.name,
            "description": template.description,
            "output_format": template.output_format,
            "section_count": len(template.sections)
        }
        for template in REPORT_TEMPLATES.values()
    ]

def get_templates_by_format(output_format: ReportFormat) -> List[ReportTemplateDefinition]:
    """Get templates that support a specific output format"""
    return [
        template for template in REPORT_TEMPLATES.values()
        if template.output_format == output_format
    ]
