"""
Intake Agent - Responsible for processing and triaging incoming tickets.
"""

from crewai import Agent

from devlifecycle_crew.config.settings import get_settings


class IntakeAgent:
    """
    The Intake Agent handles the initial processing of tickets and requests.
    
    Responsibilities:
    - Receive and parse incoming tickets/requests
    - Classify and categorize tickets
    - Assess priority and urgency
    - Route tickets to appropriate teams
    - Identify duplicates and related tickets
    """
    
    @staticmethod
    def create(tools: list = None, llm: str = None) -> Agent:
        """Create and return the Intake Agent."""
        settings = get_settings()
        
        return Agent(
            role="Ticket Intake Specialist",
            goal=(
                "Efficiently process, classify, and triage incoming development "
                "tickets to ensure they are properly categorized, prioritized, "
                "and routed to the right teams for action."
            ),
            backstory=(
                "You are an experienced intake coordinator with deep expertise in "
                "software development workflows. You've processed thousands of tickets "
                "across various domains - from bug reports to feature requests to "
                "infrastructure needs. Your keen eye for detail helps you quickly "
                "identify the nature and urgency of each request, and your knowledge "
                "of the development process ensures tickets reach the right people. "
                "You excel at asking clarifying questions and extracting essential "
                "information from vague or incomplete requests."
            ),
            tools=tools or [],
            verbose=settings.verbose,
            allow_delegation=True,
            memory=True,
        )
