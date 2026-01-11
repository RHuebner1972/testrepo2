"""
Query Builder Agent - Helps construct queries for data extraction from Creatio CRM.
"""

from crewai import Agent

from creatio_crm_crew.config.settings import get_settings


class QueryBuilderAgent:
    """
    The Query Builder Agent specializes in constructing efficient queries
    for extracting data from Creatio CRM.
    
    Responsibilities:
    - Build SQL queries for Creatio database
    - Create OData queries for Creatio API
    - Optimize query performance
    - Handle complex joins and aggregations
    - Build parameterized and reusable query templates
    - Translate business questions into technical queries
    - Support both ad-hoc and scheduled data extraction
    """
    
    @staticmethod
    def create(tools: list = None, llm: str = None) -> Agent:
        """Create and return the Query Builder Agent."""
        settings = get_settings()
        
        return Agent(
            role="Creatio CRM Query Builder Specialist",
            goal=(
                "Help users extract the exact data they need from Creatio CRM through "
                "well-crafted, efficient queries. Translate business questions into "
                "technical queries that return accurate, complete results while "
                "maintaining good performance."
            ),
            backstory=(
                "You are a database query specialist with extensive experience in "
                "Creatio CRM's data layer. You're proficient in both SQL (for direct "
                "database access) and OData (for API-based queries). You understand "
                "Creatio's entity structure, including how base entities like Contact, "
                "Account, Activity, and Opportunity are organized, and how custom "
                "entities extend this model. You're an expert at writing efficient "
                "queries that leverage proper indexing, avoid N+1 problems, and "
                "handle Creatio's specific patterns like SysAdminUnit lookups, "
                "MultiLookup columns, and Detail relationships. You can translate "
                "business questions like 'Show me all opportunities closing this "
                "quarter by account industry' into precise SQL or OData queries. "
                "You always consider query performance and suggest appropriate "
                "filtering, pagination, and caching strategies."
            ),
            tools=tools or [],
            verbose=settings.verbose,
            allow_delegation=True,
            memory=True,
        )
