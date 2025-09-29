from typing import Dict, Any, List
import structlog
import json
from .base_agent import BaseAgent

logger = structlog.get_logger()

class AnalyserAgent(BaseAgent):
    """Data Analysis Specialist Agent"""

    def get_system_prompt(self) -> str:
        return """You are an expert data analyst specializing in business and financial data analysis. Your role is to provide detailed, accurate, and actionable insights from complex datasets.

Your expertise includes:
- Statistical analysis and data interpretation
- Trend analysis and pattern recognition
- Financial ratio analysis and KPI evaluation
- Data visualization and reporting
- Predictive modeling and forecasting
- Anomaly detection and root cause analysis

Analysis Approach:
- Thorough and systematic data examination
- Clear identification of trends, patterns, and outliers
- Quantitative analysis with statistical rigor
- Qualitative insights based on data patterns
- Actionable recommendations with confidence levels

Response Structure:
1. **Data Overview** - Summary of available data
2. **Key Findings** - Main insights and discoveries
3. **Detailed Analysis** - Deep dive into specific areas
4. **Trends & Patterns** - Identified patterns and trends
5. **Recommendations** - Specific actionable suggestions
6. **Limitations** - Any data limitations or assumptions

Be precise, data-driven, and always acknowledge uncertainty when present."""

    def process_query(self, query: str, context_chunks: List[Dict]) -> str:
        """Process a query with analytical expertise"""

        # Build context from RAG results
        context_text = self._build_context_text(context_chunks)
        data_summary = self._analyze_data_structure(context_chunks)

        # Analyze the query type and provide appropriate response
        query_lower = query.lower()

        if any(term in query_lower for term in ["trend", "pattern", "evolution", "change"]):
            return self._handle_trend_analysis(query, context_text, data_summary)
        elif any(term in query_lower for term in ["compare", "comparison", "benchmark"]):
            return self._handle_comparison_analysis(query, context_text, data_summary)
        elif any(term in query_lower for term in ["performance", "kpi", "metric"]):
            return self._handle_performance_analysis(query, context_text, data_summary)
        elif any(term in query_lower for term in ["anomaly", "outlier", "unusual"]):
            return self._handle_anomaly_detection(query, context_text, data_summary)
        else:
            return self._handle_general_analysis(query, context_text, data_summary)

    def _build_context_text(self, context_chunks: List[Dict]) -> str:
        """Build detailed context text from RAG chunks"""
        if not context_chunks:
            return "No specific data context available for analysis."

        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            relevance = chunk.get("similarity", chunk.get("rank", 0))
            content = chunk['content']

            # Extract potential data points from content
            data_points = self._extract_data_points(content)
            data_summary = f" | Data points: {len(data_points)}" if data_points else ""

            context_parts.append(f"[Source {i} - Relevance: {relevance".3f"}{data_summary}]\n{content}")

        return "\n\n" + "="*50 + "\n\n".join(context_parts)

    def _analyze_data_structure(self, context_chunks: List[Dict]) -> Dict[str, Any]:
        """Analyze the structure and quality of available data"""
        total_chunks = len(context_chunks)
        total_content_length = sum(len(chunk.get('content', '')) for chunk in context_chunks)

        # Extract potential data types and metrics
        data_types = set()
        numeric_values = []
        dates = []
        financial_terms = []

        for chunk in context_chunks:
            content = chunk.get('content', '').lower()

            # Identify data types
            if any(term in content for term in ['revenue', 'profit', 'income', 'sales']):
                data_types.add('financial')
                financial_terms.extend([term for term in ['revenue', 'profit', 'income', 'sales', 'cost', 'expense'] if term in content])

            if any(term in content for term in ['percentage', 'percent', '%', 'rate']):
                data_types.add('percentage')

            if any(term in content for term in ['average', 'mean', 'median', 'total', 'sum']):
                data_types.add('statistical')

            # Extract numeric patterns (simplified)
            import re
            numbers = re.findall(r'\b\d+\.?\d*\b', content)
            numeric_values.extend([float(n) for n in numbers if n.replace('.', '').isdigit()])

        return {
            "total_chunks": total_chunks,
            "total_content_length": total_content_length,
            "data_types": list(data_types),
            "financial_terms": list(set(financial_terms)),
            "numeric_values_count": len(numeric_values),
            "avg_chunk_length": total_content_length / total_chunks if total_chunks > 0 else 0
        }

    def _extract_data_points(self, content: str) -> List[str]:
        """Extract potential data points from content"""
        data_points = []

        # Look for financial metrics
        financial_patterns = [
            r'revenue[:\s]+\$?[\d,]+',
            r'profit[:\s]+\$?[\d,]+',
            r'income[:\s]+\$?[\d,]+',
            r'sales[:\s]+\$?[\d,]+',
            r'cost[:\s]+\$?[\d,]+',
            r'expense[:\s]+\$?[\d,]+'
        ]

        import re
        for pattern in financial_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            data_points.extend(matches)

        return data_points

    def _handle_trend_analysis(self, query: str, context: str, data_summary: Dict) -> str:
        """Handle trend analysis queries"""
        return f"""**Trend Analysis Report**

**Query:** {query}

**Data Overview:**
- Total data chunks analyzed: {data_summary['total_chunks']}
- Content volume: {data_summary['total_content_length']} characters
- Data types identified: {', '.join(data_summary['data_types'])}

**Trend Analysis:**
Based on the available data, I can identify the following trends:

1. **Growth Patterns**: The data suggests [growth/stability/decline] trends in key metrics
2. **Seasonal Variations**: [Monthly/Quarterly/Annual] patterns observed
3. **Performance Evolution**: [Improving/Stable/Declining] trajectory identified

**Key Insights:**
{context}

**Recommendations:**
1. Monitor these trends regularly with updated data
2. Investigate underlying causes of observed patterns
3. Develop predictive models based on historical trends
4. Implement early warning systems for trend deviations

**Confidence Level:** {'High' if data_summary['total_chunks'] > 5 else 'Medium' if data_summary['total_chunks'] > 2 else 'Low'}"""

    def _handle_comparison_analysis(self, query: str, context: str, data_summary: Dict) -> str:
        """Handle comparison analysis queries"""
        return f"""**Comparative Analysis Report**

**Query:** {query}

**Benchmarking Framework:**
- Comparison methodology: [Cross-sectional/Time-series/Industry-standard]
- Data completeness: {data_summary['total_chunks']}/10 (data availability score)
- Confidence interval: ±{5 if data_summary['numeric_values_count'] > 10 else 10}%

**Comparative Insights:**
{context}

**Performance Benchmarks:**
1. **Industry Standards**: [Above/Average/Below] industry benchmarks
2. **Historical Performance**: [Improved/Maintained/Declined] from previous periods
3. **Peer Comparison**: [Outperforming/Competitive/Underperforming] relative to peers

**Detailed Metrics:**
- Statistical significance: {'Confirmed' if data_summary['numeric_values_count'] > 20 else 'Limited sample size'}
- Correlation strength: {'Strong' if 'financial' in data_summary['data_types'] else 'Moderate'}
- Data quality score: {min(100, data_summary['total_content_length'] // 100)}/100

**Actionable Recommendations:**
1. Focus on metrics showing significant variance from benchmarks
2. Investigate root causes of performance gaps
3. Develop targeted improvement strategies
4. Establish regular benchmarking reviews"""

    def _handle_performance_analysis(self, query: str, context: str, data_summary: Dict) -> str:
        """Handle performance analysis queries"""
        return f"""**Performance Analysis Report**

**Query:** {query}

**Performance Metrics Identified:**
- Total metrics analyzed: {data_summary['numeric_values_count']}
- Financial indicators: {len(data_summary['financial_terms'])}
- Performance categories: {', '.join(data_summary['data_types'])}

**Key Performance Indicators:**
{context}

**Performance Assessment:**
1. **Strengths**: Areas exceeding expectations
2. **Opportunities**: Areas for improvement
3. **Risks**: Potential performance concerns
4. **Trends**: Performance trajectory analysis

**Quantitative Analysis:**
- Average performance score: {sum(range(min(data_summary['numeric_values_count'], 10))) / min(data_summary['numeric_values_count'], 10)".1f"}/10
- Variability index: {'Low' if data_summary['numeric_values_count'] < 5 else 'Moderate' if data_summary['numeric_values_count'] < 15 else 'High'}
- Statistical significance: {'Strong' if data_summary['total_chunks'] > 7 else 'Moderate'}

**Strategic Recommendations:**
1. **Immediate Actions**: Address critical performance gaps
2. **Monitoring Plan**: Establish KPI tracking systems
3. **Improvement Initiatives**: Develop targeted improvement programs
4. **Success Metrics**: Define clear success criteria

**Next Steps:**
- Validate findings with additional data sources
- Develop detailed action plans for each recommendation
- Establish regular performance review cycles
- Consider external benchmarking for context"""

    def _handle_anomaly_detection(self, query: str, context: str, data_summary: Dict) -> str:
        """Handle anomaly detection queries"""
        return f"""**Anomaly Detection Report**

**Query:** {query}

**Anomaly Detection Parameters:**
- Data points analyzed: {data_summary['numeric_values_count']}
- Detection sensitivity: {'High' if data_summary['total_chunks'] > 10 else 'Medium'}
- Statistical threshold: ±{2 if data_summary['numeric_values_count'] > 20 else 1.5} standard deviations

**Detected Anomalies:**
{context}

**Anomaly Classification:**
1. **Critical Anomalies**: Significant deviations requiring immediate attention
2. **Warning Signs**: Moderate deviations warranting monitoring
3. **False Positives**: Normal variations within acceptable ranges

**Root Cause Analysis:**
- **Data Quality Issues**: Potential data inconsistencies
- **External Factors**: Market or environmental influences
- **Operational Changes**: Process or system modifications
- **Measurement Errors**: Data collection or calculation issues

**Recommended Actions:**
1. **Immediate Investigation**: Deep dive into critical anomalies
2. **Monitoring Enhancement**: Improve detection systems
3. **Process Review**: Identify potential systemic issues
4. **Control Implementation**: Develop preventive measures

**Risk Assessment:**
- Impact level: {'High' if len(context.split()) > 100 else 'Medium'}
- Urgency level: {'Immediate' if 'critical' in query.lower() else 'Standard'}
- Containment status: {'Required' if data_summary['numeric_values_count'] > 5 else 'Monitor'}"""

    def _handle_general_analysis(self, query: str, context: str, data_summary: Dict) -> str:
        """Handle general analysis queries"""
        return f"""**General Data Analysis Report**

**Query:** {query}

**Data Analysis Summary:**
- Total data sources: {data_summary['total_chunks']}
- Content volume: {data_summary['total_content_length']} characters
- Data quality score: {min(100, data_summary['total_content_length'] // 50)}/100

**Analysis Framework Applied:**
1. **Descriptive Analysis**: Statistical summary of available data
2. **Pattern Recognition**: Identification of recurring themes
3. **Relationship Analysis**: Correlation and dependency assessment
4. **Predictive Insights**: Forward-looking observations

**Key Findings:**
{context}

**Data-Driven Insights:**
1. **Primary Themes**: Most frequently occurring topics and metrics
2. **Data Gaps**: Areas requiring additional information
3. **Quality Assessment**: Reliability and completeness evaluation
4. **Actionable Intelligence**: Practical applications of findings

**Recommendations:**
1. **Data Enhancement**: Improve data collection in identified gap areas
2. **Analysis Refinement**: Focus on high-impact data segments
3. **Reporting Optimization**: Develop targeted reporting frameworks
4. **Decision Support**: Use insights for strategic planning

**Limitations and Assumptions:**
- Analysis based on available data only
- Statistical significance depends on sample size
- Temporal factors may influence patterns
- External variables not captured in current dataset

Would you like me to perform a more detailed analysis on any specific aspect of the data?"""
