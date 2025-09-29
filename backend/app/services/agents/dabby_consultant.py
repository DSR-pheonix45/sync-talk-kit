from typing import Dict, Any, List
import structlog
from .base_agent import BaseAgent

logger = structlog.get_logger()

class DabbyConsultantAgent(BaseAgent):
    """Dabby - Business Financial Consultant Agent"""

    def get_system_prompt(self) -> str:
        return """You are Dabby, an expert business and financial consultant with over 15 years of experience helping companies optimize their financial performance and strategic decision-making.

Your expertise includes:
- Financial analysis and modeling
- Business strategy and planning
- Risk assessment and mitigation
- Performance optimization
- Market analysis and competitive positioning
- Financial reporting and KPI tracking

Communication Style:
- Professional yet approachable
- Clear and actionable advice
- Focus on practical solutions
- Use business terminology appropriately
- Always provide specific recommendations

When responding:
1. Acknowledge the user's specific situation
2. Provide clear, actionable insights
3. Support recommendations with data when available
4. Suggest next steps or implementation strategies
5. Offer to dive deeper into specific areas

Remember: You are Dabby, the trusted financial consultant. Be confident in your expertise but humble in your approach."""

    def process_query(self, query: str, context_chunks: List[Dict]) -> str:
        """Process a query with Dabby's consultant expertise"""

        # Build context from RAG results
        context_text = self._build_context_text(context_chunks)

        # Analyze the query type and provide appropriate response
        query_lower = query.lower()

        if any(term in query_lower for term in ["financial", "revenue", "profit", "cash flow", "budget"]):
            return self._handle_financial_query(query, context_text)
        elif any(term in query_lower for term in ["strategy", "plan", "growth", "expansion"]):
            return self._handle_strategy_query(query, context_text)
        elif any(term in query_lower for term in ["risk", "analysis", "assessment"]):
            return self._handle_risk_query(query, context_text)
        else:
            return self._handle_general_query(query, context_text)

    def _build_context_text(self, context_chunks: List[Dict]) -> str:
        """Build context text from RAG chunks"""
        if not context_chunks:
            return ""

        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            relevance = chunk.get("similarity", chunk.get("rank", 0))
            context_parts.append(f"[Source {i} - Relevance: {relevance".2f"}] {chunk['content']}")

        return "\n\n".join(context_parts)

    def _handle_financial_query(self, query: str, context: str) -> str:
        """Handle financial-related queries"""
        base_response = f"""Based on my analysis of your financial data and the available context, here are my key insights:

"""

        if context:
            base_response += f"""
**Data Analysis:**
{context}

"""

        base_response += """
**Key Recommendations:**
1. **Focus on Cash Flow Management** - Ensure positive cash flow through efficient working capital management
2. **Revenue Optimization** - Identify and capitalize on high-margin revenue streams
3. **Cost Control** - Implement regular cost-benefit analysis for all expenses
4. **Financial Planning** - Develop 3-5 year financial projections with scenario planning

**Next Steps:**
- Review your current financial statements in detail
- Identify key performance indicators (KPIs) to track
- Consider implementing financial management software if not already in place

Would you like me to dive deeper into any specific financial area or help you develop an action plan?"""

        return base_response

    def _handle_strategy_query(self, query: str, context: str) -> str:
        """Handle strategy-related queries"""
        base_response = """As your strategic business consultant, let me provide you with strategic insights based on the available data:

"""

        if context:
            base_response += f"""
**Strategic Context:**
{context}

"""

        base_response += """
**Strategic Recommendations:**
1. **Market Positioning** - Clearly define your competitive advantage and target market
2. **Growth Strategy** - Develop a sustainable growth plan with clear milestones
3. **Operational Excellence** - Streamline processes to improve efficiency and reduce costs
4. **Innovation Focus** - Allocate resources for continuous improvement and innovation

**Implementation Framework:**
- Set clear strategic objectives with measurable outcomes
- Develop detailed action plans with timelines and responsibilities
- Establish regular review cycles to track progress
- Be prepared to adapt strategies based on market feedback

What specific strategic area would you like to explore further?"""

        return base_response

    def _handle_risk_query(self, query: str, context: str) -> str:
        """Handle risk assessment queries"""
        base_response = """Let me help you assess and mitigate business risks based on the available information:

"""

        if context:
            base_response += f"""
**Risk Context:**
{context}

"""

        base_response += """
**Risk Assessment Framework:**
1. **Financial Risks** - Cash flow, market volatility, credit risks
2. **Operational Risks** - Process inefficiencies, supply chain disruptions
3. **Strategic Risks** - Competitive threats, market changes, regulatory changes
4. **Compliance Risks** - Legal, regulatory, and governance requirements

**Risk Mitigation Strategies:**
- Diversify revenue streams and customer base
- Implement robust internal controls and monitoring systems
- Develop contingency plans for various risk scenarios
- Regular risk assessments and updates to risk management plans

**Priority Actions:**
1. Conduct comprehensive risk assessment
2. Develop risk mitigation strategies
3. Implement monitoring and early warning systems
4. Create response plans for high-impact risks

Would you like me to help you develop a specific risk management plan or assess a particular risk area?"""

        return base_response

    def _handle_general_query(self, query: str, context: str) -> str:
        """Handle general business queries"""
        base_response = """Thank you for your question. As Dabby, your business financial consultant, let me provide you with professional insights:

"""

        if context:
            base_response += f"""
**Relevant Information:**
{context}

"""

        base_response += """
**General Business Advice:**
1. **Data-Driven Decisions** - Always base decisions on solid data and analysis
2. **Continuous Learning** - Stay updated with industry trends and best practices
3. **Stakeholder Communication** - Keep all stakeholders informed and engaged
4. **Long-term Perspective** - Balance short-term needs with long-term sustainability

**Professional Recommendations:**
- Regularly review and update your business plan
- Build strong relationships with key stakeholders
- Invest in employee development and training
- Maintain financial discipline and strategic focus

How can I assist you further with your business needs?"""

        return base_response
