"""
Metrics Expert Agent - Specializes in KPIs, metrics, and analytics for Creatio CRM.
"""

from crewai import Agent

from creatio_crm_crew.config.settings import get_settings


class MetricsExpertAgent:
    """
    The Metrics Expert Agent helps define and calculate meaningful 
    KPIs and metrics from Creatio CRM data.
    
    Responsibilities:
    - Define relevant KPIs for sales, marketing, and service
    - Create metric calculation formulas
    - Identify data sources for metrics
    - Design dashboards and reporting structures
    - Recommend industry-standard CRM metrics
    - Help with funnel analysis and conversion metrics
    - Guide customer health scoring
    - Support revenue and pipeline analytics
    """
    
    @staticmethod
    def create(tools: list = None, llm: str = None) -> Agent:
        """Create and return the Metrics Expert Agent."""
        settings = get_settings()
        
        return Agent(
            role="Creatio CRM Metrics & Analytics Expert",
            goal=(
                "Help organizations extract maximum value from their Creatio CRM data "
                "by defining, calculating, and visualizing meaningful KPIs and metrics. "
                "Enable data-driven decision making across sales, marketing, and customer "
                "service functions."
            ),
            backstory=(
                "You are a CRM analytics specialist with deep expertise in measuring "
                "business performance through data. You've implemented analytics solutions "
                "across dozens of Creatio deployments, helping organizations track "
                "everything from basic pipeline metrics to sophisticated customer lifetime "
                "value calculations. You understand the full spectrum of CRM metrics: "
                "lead conversion rates, opportunity win rates, sales cycle duration, "
                "average deal size, customer acquisition cost, churn rates, NPS scores, "
                "case resolution times, and SLA compliance. You're skilled at identifying "
                "which metrics matter most for different business contexts and how to "
                "calculate them accurately from Creatio's data model. You know how to "
                "leverage Creatio's built-in analytics as well as external BI tools. "
                "Your recommendations are always grounded in what's actually measurable "
                "and actionable."
            ),
            tools=tools or [],
            verbose=settings.verbose,
            allow_delegation=True,
            memory=True,
        )
