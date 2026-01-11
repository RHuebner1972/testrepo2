"""
Schema Analyst Agent - Responsible for analyzing and explaining Creatio CRM database schema.
"""

from crewai import Agent

from creatio_crm_crew.config.settings import get_settings


class SchemaAnalystAgent:
    """
    The Schema Analyst Agent specializes in understanding and explaining 
    Creatio CRM's database structure.
    
    Responsibilities:
    - Explore and document database tables and relationships
    - Explain entity relationships and data flows
    - Identify primary/foreign key relationships
    - Document column types, constraints, and purposes
    - Map business objects to database tables
    - Identify lookup tables and reference data
    - Explain Creatio's object model and inheritance patterns
    """
    
    @staticmethod
    def create(tools: list = None, llm: str = None) -> Agent:
        """Create and return the Schema Analyst Agent."""
        settings = get_settings()
        
        return Agent(
            role="Creatio CRM Schema Analyst",
            goal=(
                "Provide comprehensive understanding of the Creatio CRM database schema, "
                "making complex data structures accessible to data architects and staff. "
                "Help users understand entity relationships, data flows, and how business "
                "concepts map to the underlying database structure."
            ),
            backstory=(
                "You are an expert database analyst with deep knowledge of Creatio CRM's "
                "architecture and data model. You've spent years working with Creatio "
                "implementations across various industries, understanding how the platform "
                "structures data for contacts, accounts, opportunities, activities, and "
                "custom objects. You're familiar with Creatio's object model, including "
                "the base entity schema, lookup patterns, and detail relationships. "
                "You excel at translating technical database structures into business-"
                "friendly explanations, helping both technical and non-technical users "
                "understand how their data is organized. You know the common tables like "
                "Contact, Account, Activity, Opportunity, Lead, Case, and how they "
                "interconnect through the CRM's relationship model."
            ),
            tools=tools or [],
            verbose=settings.verbose,
            allow_delegation=True,
            memory=True,
        )
