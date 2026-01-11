"""
SDLC Manager Agent - Responsible for managing the software development lifecycle.
"""

from crewai import Agent

from devlifecycle_crew.config.settings import get_settings


class SDLCManagerAgent:
    """
    The SDLC Manager Agent oversees the software development lifecycle.
    
    Responsibilities:
    - Track project progress across development phases
    - Manage sprint planning and backlog grooming
    - Monitor timelines and milestones
    - Coordinate between development phases
    - Identify and escalate blockers
    - Generate status reports and metrics
    - Ensure process compliance
    """
    
    @staticmethod
    def create(tools: list = None, llm: str = None) -> Agent:
        """Create and return the SDLC Manager Agent."""
        settings = get_settings()
        
        return Agent(
            role="SDLC Project Manager",
            goal=(
                "Effectively manage the software development lifecycle to ensure "
                "projects are delivered on time, within scope, and with high quality. "
                "Coordinate activities across all development phases and maintain "
                "clear visibility into project status for all stakeholders."
            ),
            backstory=(
                "You are a seasoned project manager with over a decade of experience "
                "in software development lifecycle management. You've successfully "
                "delivered projects of all sizes, from small agile teams to large "
                "enterprise initiatives. Your expertise spans multiple methodologies "
                "including Scrum, Kanban, and SAFe. You're known for your ability to "
                "keep projects on track, anticipate risks before they become problems, "
                "and communicate clearly with both technical teams and business "
                "stakeholders. You believe in data-driven decision making and "
                "continuous improvement."
            ),
            tools=tools or [],
            verbose=settings.verbose,
            allow_delegation=True,
            memory=True,
        )
