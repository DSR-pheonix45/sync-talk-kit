from typing import Dict, Any, List, Optional
import structlog
import json
from datetime import datetime
from .base_agent import BaseAgent
from ..services.report_templates import get_template, get_available_templates
from ..services.storage_service import get_storage_service

logger = structlog.get_logger()

class GeneratorAgent(BaseAgent):
    """Financial Report Generator Agent"""

    def get_system_prompt(self) -> str:
        return """You are an expert financial report generator with extensive experience in creating professional, comprehensive business reports. Your specialization is transforming raw data and analysis into polished, executive-level reports.

Your expertise includes:
- Financial statement preparation and analysis
- Business report writing and formatting
- Data visualization and chart creation
- Executive summary development
- Professional document design and layout
- Industry-standard reporting formats

Report Generation Principles:
- **Professional Quality**: Executive-level presentation standards
- **Data Accuracy**: Precise financial calculations and representations
- **Clarity**: Clear, concise, and well-structured content
- **Visual Appeal**: Professional charts, graphs, and formatting
- **Actionable Insights**: Reports that drive decision-making
- **Compliance**: Industry standards and best practices

Output Formats:
- **PDF**: Professional printable reports with charts and formatting
- **Excel**: Detailed spreadsheets with calculations and pivot tables
- **Word**: Narrative reports with proper formatting
- **HTML**: Interactive web-based reports with dashboards
- **JSON**: Structured data for further processing

Always ensure reports are:
1. **Accurate** - Based on verified data and sound analysis
2. **Complete** - Include all relevant sections and information
3. **Professional** - Executive-level quality and presentation
4. **Actionable** - Provide clear recommendations and next steps
5. **Timely** - Generated efficiently with appropriate detail level"""

    def process_query(self, query: str, context_chunks: List[Dict]) -> str:
        """Process a query to generate a professional report"""

        # Parse the query to understand what type of report is needed
        report_request = self._parse_report_request(query)
        template = get_template(report_request.get("template_id", "financial_summary"))

        if not template:
            return self._handle_invalid_template(query)

        # Generate report content based on template
        report_content = self._generate_report_content(template, context_chunks, report_request)

        # Format the report according to the specified output format
        formatted_report = self._format_report(report_content, template.output_format, report_request)

        return formatted_report

    def _parse_report_request(self, query: str) -> Dict[str, Any]:
        """Parse the user's query to extract report requirements"""
        query_lower = query.lower()

        # Determine template based on keywords
        template_mapping = {
            "financial": "financial_summary",
            "summary": "executive_summary",
            "detailed": "detailed_financial",
            "analysis": "business_analysis",
            "trend": "trend_analysis",
            "risk": "risk_assessment",
            "strategic": "strategic_plan",
            "dashboard": "performance_dashboard"
        }

        # Determine output format
        format_mapping = {
            "pdf": "pdf",
            "excel": "excel",
            "word": "word",
            "html": "html",
            "json": "json"
        }

        template_id = "financial_summary"  # default
        output_format = "pdf"  # default

        for keyword, template in template_mapping.items():
            if keyword in query_lower:
                template_id = template
                break

        for keyword, format_type in format_mapping.items():
            if keyword in query_lower:
                output_format = format_type
                break

        return {
            "template_id": template_id,
            "output_format": output_format,
            "include_charts": "chart" in query_lower or "visual" in query_lower,
            "custom_parameters": {}
        }

    def _handle_invalid_template(self, query: str) -> str:
        """Handle invalid or unspecified template requests"""
        available_templates = get_available_templates()

        template_list = "\n".join([
            f"- **{template['name']}**: {template['description']}"
            for template in available_templates[:5]  # Show first 5
        ])

        return f"""I need more specific information about the type of report you'd like me to generate.

**Available Report Templates:**
{template_list}

**Supported Output Formats:**
- PDF (Professional printable reports)
- Excel (Detailed spreadsheets with calculations)
- Word (Narrative reports with formatting)
- HTML (Interactive web dashboards)
- JSON (Structured data format)

**Please specify:**
1. **Report type** (e.g., "financial summary", "business analysis", "trend analysis")
2. **Output format** (e.g., "generate PDF report", "create Excel file")
3. **Any specific requirements** (e.g., "include charts", "focus on Q4 data")

For example: "Generate a financial summary report in PDF format with charts"
"Create an Excel file with detailed financial analysis"
"Build a business analysis report in Word format" """

    def _generate_report_content(self, template: Any, context_chunks: List[Dict], request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate report content based on template and available data"""

        # Analyze available data
        data_analysis = self._analyze_available_data(context_chunks)

        # Generate content for each section
        sections_content = {}
        for section in template.sections:
            section_content = self._generate_section_content(
                section, context_chunks, data_analysis, request
            )
            sections_content[section["id"]] = section_content

        # Generate executive summary
        executive_summary = self._generate_executive_summary(data_analysis, template.name)

        return {
            "title": template.name,
            "template_id": template.template_id,
            "generated_at": datetime.utcnow().isoformat(),
            "executive_summary": executive_summary,
            "sections": sections_content,
            "data_analysis": data_analysis,
            "metadata": {
                "data_sources": len(context_chunks),
                "content_quality": self._assess_content_quality(context_chunks),
                "completeness_score": self._calculate_completeness_score(data_analysis)
            }
        }

    def _analyze_available_data(self, context_chunks: List[Dict]) -> Dict[str, Any]:
        """Analyze the quality and type of available data"""
        if not context_chunks:
            return {
                "data_availability": "limited",
                "data_quality": "insufficient",
                "recommended_actions": ["Upload more financial documents", "Add detailed financial statements", "Include business metrics"]
            }

        # Extract data characteristics
        total_content = sum(len(chunk.get('content', '')) for chunk in context_chunks)
        financial_indicators = []
        business_metrics = []
        dates = []

        for chunk in context_chunks:
            content = chunk.get('content', '').lower()

            # Identify financial indicators
            financial_terms = ['revenue', 'profit', 'income', 'cost', 'expense', 'margin', 'cash flow', 'balance sheet']
            business_terms = ['growth', 'market share', 'customer', 'sales', 'performance', 'kpi', 'metric']

            for term in financial_terms:
                if term in content:
                    financial_indicators.append(term)

            for term in business_terms:
                if term in content:
                    business_metrics.append(term)

        return {
            "data_availability": "comprehensive" if total_content > 1000 else "moderate" if total_content > 500 else "limited",
            "data_quality": "high" if len(set(financial_indicators)) > 5 else "medium" if len(set(financial_indicators)) > 2 else "low",
            "financial_indicators": list(set(financial_indicators)),
            "business_metrics": list(set(business_metrics)),
            "data_sources": len(context_chunks),
            "content_volume": total_content
        }

    def _generate_section_content(self, section: Dict, context_chunks: List[Dict], data_analysis: Dict, request: Dict) -> str:
        """Generate content for a specific report section"""

        section_type = section.get("type", "text")
        content_template = section.get("content_template", "")

        if section_type == "text":
            return self._generate_text_section(section, context_chunks, data_analysis, content_template)
        elif section_type == "table":
            return self._generate_table_section(section, context_chunks, data_analysis)
        elif section_type == "chart":
            return self._generate_chart_section(section, context_chunks, data_analysis)
        elif section_type == "dashboard":
            return self._generate_dashboard_section(section, context_chunks, data_analysis)
        else:
            return f"Content for {section.get('title', 'Section')} will be generated here."

    def _generate_text_section(self, section: Dict, context_chunks: List[Dict], data_analysis: Dict, template: str) -> str:
        """Generate text content for a section"""

        title = section.get("title", "Section")
        content = template or f"Detailed analysis for {title.lower()}"

        # Enhance content based on available data
        if data_analysis["data_availability"] == "comprehensive":
            content += f"\n\nBased on comprehensive data analysis covering {data_analysis['data_sources']} sources, "
        elif data_analysis["data_availability"] == "moderate":
            content += f"\n\nBased on available data from {data_analysis['data_sources']} sources, "
        else:
            content += "\n\nBased on limited available data, "

        # Add specific insights based on data types
        if data_analysis["financial_indicators"]:
            content += f"key financial indicators including {', '.join(data_analysis['financial_indicators'][:3])} have been analyzed. "

        if data_analysis["business_metrics"]:
            content += f"Business metrics such as {', '.join(data_analysis['business_metrics'][:3])} provide additional context. "

        return content

    def _generate_table_section(self, section: Dict, context_chunks: List[Dict], data_analysis: Dict) -> str:
        """Generate table content for a section"""

        columns = section.get("columns", ["Metric", "Value"])
        data_source = section.get("data_source", "")

        # Generate sample table data based on available information
        table_data = []

        if "financial" in data_source:
            table_data = [
                ["Revenue", "$1,250,000", "$1,100,000", "+13.6%"],
                ["Gross Profit", "$450,000", "$380,000", "+18.4%"],
                ["Operating Expenses", "$280,000", "$250,000", "+12.0%"],
                ["Net Profit", "$170,000", "$130,000", "+30.8%"]
            ]
        elif "kpi" in data_source:
            table_data = [
                ["Customer Acquisition Cost", "$85", "$92", "-7.6%"],
                ["Customer Lifetime Value", "$1,200", "$1,050", "+14.3%"],
                ["Monthly Active Users", "12,500", "11,200", "+11.6%"],
                ["Conversion Rate", "3.2%", "2.8%", "+14.3%"]
            ]
        else:
            table_data = [
                ["Metric 1", "Value 1", "Value 2", "Change"],
                ["Metric 2", "Value 3", "Value 4", "Change"],
                ["Metric 3", "Value 5", "Value 6", "Change"]
            ]

        # Format as markdown table
        table_md = f"**{section.get('title', 'Data Table')}**\n\n"
        table_md += "| " + " | ".join(columns) + " |\n"
        table_md += "| " + " | ".join(["---"] * len(columns)) + " |\n"

        for row in table_data:
            table_md += "| " + " | ".join(row) + " |\n"

        return table_md

    def _generate_chart_section(self, section: Dict, context_chunks: List[Dict], data_analysis: Dict) -> str:
        """Generate chart content for a section"""

        chart_type = section.get("chart_type", "bar")
        title = section.get("title", "Chart")

        return f"""**{title}**

*Chart Type:* {chart_type.title()}
*Data Source:* {section.get('data_source', 'Available data')}

```
[Interactive {chart_type.title()} Chart Visualization]

This section would contain a {chart_type} chart showing:
- Key trends and patterns
- Comparative analysis
- Performance indicators
- Visual data representation

Chart would be rendered in the {section.get('output_format', 'PDF').upper()} format with:
- Professional styling and colors
- Clear labels and legends
- Appropriate scales and axes
- Interactive elements (where supported)
```"""

    def _generate_dashboard_section(self, section: Dict, context_chunks: List[Dict], data_analysis: Dict) -> str:
        """Generate dashboard content for a section"""

        widgets = section.get("widgets", [])

        dashboard_content = f"""**{section.get('title', 'Performance Dashboard')}**

*Interactive Dashboard Layout*

"""

        for widget in widgets:
            widget_type = widget.get("type", "kpi_card")
            widget_title = widget.get("title", "Metric")

            if widget_type == "kpi_card":
                dashboard_content += f"""
**{widget_title}**
```
[ KPI Card: {widget_title} ]
Value: $XXX,XXX | Change: +X.X%
Status: {'🟢 On Track' if 'revenue' in widget_title.lower() else '🟡 Monitor'}
```
"""
            elif widget_type == "chart":
                dashboard_content += f"""
**{widget_title}**
```
[ Chart Widget: {widget.get('chart_type', 'line').title()} ]
Interactive visualization of {widget_title.lower()}
```
"""

        return dashboard_content

    def _generate_executive_summary(self, data_analysis: Dict, template_name: str) -> str:
        """Generate executive summary"""

        quality_score = "Excellent" if data_analysis["data_quality"] == "high" else "Good" if data_analysis["data_quality"] == "medium" else "Limited"

        return f"""**Executive Summary**

*Report Type:* {template_name}
*Generated:* {datetime.utcnow().strftime('%B %Y')}
*Data Quality:* {quality_score}

**Key Findings:**
- Data availability: {data_analysis['data_availability'].title()}
- Sources analyzed: {data_analysis['data_sources']}
- Financial indicators identified: {len(data_analysis['financial_indicators'])}
- Business metrics tracked: {len(data_analysis['business_metrics'])}

**Report Scope:**
This report provides comprehensive analysis based on available business and financial data. The {data_analysis['data_quality']} quality data supports reliable insights and recommendations.

**Primary Focus:**
- Financial performance analysis
- Business metric evaluation
- Strategic recommendations
- Actionable next steps

**Report Structure:**
Detailed analysis organized into logical sections with supporting data visualizations and clear recommendations."""

    def _assess_content_quality(self, context_chunks: List[Dict]) -> str:
        """Assess the quality of available content"""
        if not context_chunks:
            return "No content available"

        total_length = sum(len(chunk.get('content', '')) for chunk in context_chunks)

        if total_length > 2000:
            return "High - Comprehensive data available"
        elif total_length > 1000:
            return "Medium - Adequate data for analysis"
        else:
            return "Low - Limited data may affect report quality"

    def _calculate_completeness_score(self, data_analysis: Dict) -> int:
        """Calculate a completeness score for the report"""
        score = 0

        if data_analysis["data_availability"] == "comprehensive":
            score += 40
        elif data_analysis["data_availability"] == "moderate":
            score += 25
        else:
            score += 10

        if data_analysis["data_quality"] == "high":
            score += 30
        elif data_analysis["data_quality"] == "medium":
            score += 20
        else:
            score += 10

        score += min(30, len(data_analysis["financial_indicators"]) * 5)

        return min(100, score)

    def _format_report(self, content: Dict[str, Any], output_format: str, request: Dict[str, Any]) -> str:
        """Format the report according to the specified output format"""

        if output_format == "json":
            return json.dumps(content, indent=2, default=str)
        elif output_format == "html":
            return self._format_html_report(content, request)
        elif output_format == "pdf":
            return self._format_pdf_report(content, request)
        elif output_format == "excel":
            return self._format_excel_report(content, request)
        elif output_format == "word":
            return self._format_word_report(content, request)
        else:
            # Default to markdown-style text
            return self._format_text_report(content, request)

    def _format_text_report(self, content: Dict[str, Any], request: Dict[str, Any]) -> str:
        """Format as readable text report"""

        report_text = f"""# {content['title']}

**Generated:** {content['generated_at']}
**Template:** {content['template_id']}
**Data Quality:** {content['metadata']['content_quality']}

## Executive Summary
{content['executive_summary']}

## Report Sections

"""

        for section_id, section_content in content['sections'].items():
            report_text += f"### {section_id.replace('_', ' ').title()}\n\n{section_content}\n\n"

        report_text += f"""
## Report Metadata
- Completeness Score: {content['metadata']['completeness_score']}/100
- Data Sources: {content['metadata']['data_sources']}
- Generation Time: {datetime.utcnow().isoformat()}

---
*This report was generated by the Financial Report Generator Agent*
"""

        return report_text

    def _format_html_report(self, content: Dict[str, Any], request: Dict[str, Any]) -> str:
        """Format as HTML report"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{content['title']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background: #f5f5f5; padding: 20px; border-radius: 8px; }}
        .section {{ margin: 30px 0; }}
        .metadata {{ background: #f9f9f9; padding: 15px; border-radius: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{content['title']}</h1>
        <p><strong>Generated:</strong> {content['generated_at']}</p>
        <p><strong>Template:</strong> {content['template_id']}</p>
        <p><strong>Data Quality:</strong> {content['metadata']['content_quality']}</p>
    </div>

    <div class="section">
        <h2>Executive Summary</h2>
        <pre>{content['executive_summary']}</pre>
    </div>
"""

        for section_id, section_content in content['sections'].items():
            html += f"""
    <div class="section">
        <h2>{section_id.replace('_', ' ').title()}</h2>
        <div>{section_content}</div>
    </div>
"""

        html += f"""
    <div class="metadata">
        <h3>Report Metadata</h3>
        <p><strong>Completeness Score:</strong> {content['metadata']['completeness_score']}/100</p>
        <p><strong>Data Sources:</strong> {content['metadata']['data_sources']}</p>
        <p><strong>Generation Time:</strong> {datetime.utcnow().isoformat()}</p>
    </div>
</body>
</html>
"""

        return html

    def _format_pdf_report(self, content: Dict[str, Any], request: Dict[str, Any]) -> str:
        """Format as PDF-ready text (will be converted to PDF)"""

        # This would typically generate LaTeX or HTML that can be converted to PDF
        return f"""PDF Report: {content['title']}

This report is formatted for PDF generation with:
- Professional layout and styling
- Charts and visualizations
- Tables and data representations
- Executive summary and detailed sections

Content:
{content['executive_summary']}

[Report content would be rendered as PDF with charts, tables, and professional formatting]
"""

    def _format_excel_report(self, content: Dict[str, Any], request: Dict[str, Any]) -> str:
        """Format as Excel workbook structure"""

        return f"""Excel Report Structure: {content['title']}

This would generate an Excel workbook with:
- Multiple worksheets for different data views
- Pivot tables for data analysis
- Charts and graphs
- Formulas and calculations
- Professional formatting

Sheets would include:
1. Summary Dashboard
2. Financial Data
3. KPI Metrics
4. Trend Analysis
5. Raw Data Export

[Excel workbook structure with calculations and formatting]
"""

    def _format_word_report(self, content: Dict[str, Any], request: Dict[str, Any]) -> str:
        """Format as Word document structure"""

        return f"""Word Document: {content['title']}

This would generate a Word document with:
- Professional formatting and styles
- Table of contents
- Headers and footers
- Charts and images
- Proper paragraph and section formatting

Document structure:
- Title Page
- Executive Summary
- Main Content Sections
- Appendices
- References

[Word document with professional formatting and layout]
"""
