"""Task definitions for the DevLifecycle Crew."""

from devlifecycle_crew.tasks.intake_tasks import IntakeTasks
from devlifecycle_crew.tasks.requirements_tasks import RequirementsTasks
from devlifecycle_crew.tasks.sdlc_tasks import SDLCTasks
from devlifecycle_crew.tasks.quality_tasks import QualityTasks
from devlifecycle_crew.tasks.planning_tasks import PlanningTasks

__all__ = [
    "IntakeTasks",
    "RequirementsTasks",
    "SDLCTasks",
    "QualityTasks",
    "PlanningTasks",
]
