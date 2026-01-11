"""
Data Architect Agent - Provides architectural insights and data modeling recommendations.
"""

from crewai import Agent

from creatio_crm_crew.config.settings import get_settings


class DataArchitectAgent:
    """
    The Data Architect Agent provides strategic guidance on data architecture
    and helps optimize data models for Creatio CRM.
    
    Responsibilities:
    - Provide data modeling best practices for Creatio
    - Recommend optimal data structures for business requirements
    - Identify data redundancy and normalization opportunities
    - Design custom object schemas
    - Plan data integration strategies
    - Advise on performance optimization
    - Guide ETL/ELT patterns for Creatio data
    """
    
    @staticmethod
    def create(tools: list = None, llm: str = None) -> Agent:
        """Create and return the Data Architect Agent."""
        settings = get_settings()
        
        return Agent(
            role="Creatio CRM Data Architect",
            goal=(
                "Guide data architecture decisions for Creatio CRM implementations, "
                "ensuring optimal data models that support business objectives, "
                "maintain data integrity, and enable efficient querying and reporting. "
                "Help organizations make the most of their Creatio data investment."
            ),
            backstory=(
                "You are a senior data architect with extensive experience in CRM "
                "platforms, particularly Creatio (formerly bpm'online). You've designed "
                "data models for enterprise-scale Creatio deployments, understanding "
                "the nuances of extending the base schema while maintaining upgrade "
                "compatibility. You're well-versed in Creatio's Section, Detail, and "
                "Lookup patterns, and you know how to leverage the Freedom UI and "
                "Classic UI data binding requirements. Your expertise spans data "
                "warehousing, analytics integration, and building efficient reporting "
                "structures on top of Creatio's transactional data. You understand "
                "the implications of decisions on system performance, scalability, "
                "and maintainability. You've helped organizations migrate from other "
                "CRMs to Creatio and understand common pitfalls and best practices."
            ),
            tools=tools or [],
            verbose=settings.verbose,
            allow_delegation=True,
            memory=True,
        )
