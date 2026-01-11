"""
Planning Agent - Responsible for sprint and release planning.
"""

from crewai import Agent

from devlifecycle_crew.config.settings import get_settings


class PlanningAgent:
    """
    The Planning Agent handles sprint and release planning activities.
    
    Responsibilities:
    - Estimate effort and complexity for tickets
    - Plan sprints and allocate work
    - Balance workload across team members
    - Sequence dependencies appropriately
    - Plan releases and milestones
    - Optimize for team velocity and capacity
    """
    
    @staticmethod
    def create(tools: list = None, llm: str = None) -> Agent:
        """Create and return the Planning Agent."""
        settings = get_settings()
        
        return Agent(
            role="Sprint & Release Planner",
            goal=(
                "Create optimal sprint and release plans that maximize value delivery "
                "while respecting team capacity and dependencies. Ensure sustainable "
                "development pace and predictable delivery timelines."
            ),
            backstory=(
                "You are an expert in agile planning and estimation with a strong "
                "background in software development. You understand the challenges "
                "of estimating software work and have developed techniques to improve "
                "accuracy over time. You're skilled at breaking down large initiatives "
                "into manageable chunks, identifying dependencies, and creating "
                "realistic plans that teams can actually deliver. You balance the "
                "pressure for speed with the need for sustainable development "
                "practices. Your sprint plans consistently achieve high completion "
                "rates because you account for real-world factors like meetings, "
                "support work, and unexpected issues."
            ),
            tools=tools or [],
            verbose=settings.verbose,
            allow_delegation=False,
            memory=True,
        )
