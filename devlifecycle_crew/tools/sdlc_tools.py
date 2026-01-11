"""
SDLC management tools for the DevLifecycle Crew.
"""

from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class SprintPlanInput(BaseModel):
    """Input schema for sprint planning."""
    sprint_name: str = Field(description="Name or number of the sprint")
    capacity: int = Field(description="Team capacity in story points")
    items: str = Field(description="Comma-separated list of item IDs to consider")


class StatusInput(BaseModel):
    """Input schema for status tracking."""
    project_id: str = Field(
        default="default",
        description="Project identifier"
    )
    include_details: bool = Field(
        default=True,
        description="Whether to include detailed breakdown"
    )


class RiskInput(BaseModel):
    """Input schema for risk assessment."""
    scope: str = Field(description="What to assess: project, sprint, release, feature")
    context: str = Field(description="Additional context for assessment")


class SprintPlannerTool(BaseTool):
    """Tool for sprint planning assistance."""
    
    name: str = "sprint_planner"
    description: str = (
        "Assists with sprint planning by analyzing capacity, "
        "prioritizing items, and suggesting optimal sprint composition. "
        "Considers dependencies, team velocity, and business priorities."
    )
    args_schema: Type[BaseModel] = SprintPlanInput
    
    def _run(
        self,
        sprint_name: str,
        capacity: int,
        items: str
    ) -> str:
        """Generate sprint plan."""
        item_list = [i.strip() for i in items.split(",") if i.strip()]
        
        # In a real implementation, this would analyze actual backlog items
        plan_result = {
            "success": True,
            "sprint": sprint_name,
            "capacity": capacity,
            "planned_points": int(capacity * 0.85),  # 85% utilization
            "buffer_points": int(capacity * 0.15),
            "items_considered": len(item_list),
            "recommended_items": item_list[:5] if len(item_list) > 5 else item_list,
            "deferred_items": item_list[5:] if len(item_list) > 5 else [],
            "sprint_goal": f"Complete core functionality for {sprint_name}",
            "risks": [
                "External dependency on API team",
                "New team member ramping up"
            ],
            "recommendations": [
                "Start with highest-priority items",
                "Reserve time for code review",
                "Plan mid-sprint check-in"
            ]
        }
        
        return str(plan_result)


class StatusTrackerTool(BaseTool):
    """Tool for tracking project status."""
    
    name: str = "status_tracker"
    description: str = (
        "Retrieves current status of sprints, releases, and projects. "
        "Provides metrics on progress, velocity, and health indicators. "
        "Use for status reports and decision-making."
    )
    args_schema: Type[BaseModel] = StatusInput
    
    def _run(
        self,
        project_id: str = "default",
        include_details: bool = True
    ) -> str:
        """Get project status."""
        # In a real implementation, this would query project management systems
        
        status = {
            "success": True,
            "project_id": project_id,
            "overall_health": "on_track",  # on_track, at_risk, behind
            "current_sprint": {
                "name": "Sprint 5",
                "progress": 65,
                "days_remaining": 5,
                "committed_points": 34,
                "completed_points": 22,
                "in_progress_points": 8,
                "blocked_points": 4
            },
            "velocity": {
                "average": 32,
                "last_sprint": 34,
                "trend": "stable"
            },
            "release_progress": {
                "name": "Release 2.0",
                "features_total": 12,
                "features_done": 7,
                "features_in_progress": 3,
                "target_date": "2026-02-15",
                "confidence": "medium"
            },
            "blockers": [
                {
                    "id": "BLOCK-001",
                    "description": "Waiting for API documentation",
                    "age_days": 3,
                    "owner": "External Team"
                }
            ],
            "recent_completions": [
                "US-042: User authentication",
                "US-043: Dashboard redesign"
            ]
        }
        
        if not include_details:
            # Simplified status
            status = {
                "success": True,
                "project_id": project_id,
                "overall_health": status["overall_health"],
                "sprint_progress": status["current_sprint"]["progress"],
                "blockers_count": len(status["blockers"])
            }
        
        return str(status)


class RiskAssessmentTool(BaseTool):
    """Tool for assessing project risks."""
    
    name: str = "risk_assessment"
    description: str = (
        "Performs risk assessment for projects, sprints, releases, or features. "
        "Identifies potential risks, assesses probability and impact, "
        "and suggests mitigation strategies."
    )
    args_schema: Type[BaseModel] = RiskInput
    
    def _run(self, scope: str, context: str) -> str:
        """Assess risks."""
        # In a real implementation, this would perform actual risk analysis
        
        assessment = {
            "success": True,
            "scope": scope,
            "assessment_date": "2026-01-10",
            "overall_risk_level": "medium",
            "risks": [
                {
                    "id": "RISK-001",
                    "category": "technical",
                    "description": "Integration complexity with legacy system",
                    "probability": "medium",
                    "impact": "high",
                    "risk_score": 6,
                    "mitigation": "Early POC and incremental integration",
                    "owner": "Tech Lead",
                    "status": "monitoring"
                },
                {
                    "id": "RISK-002",
                    "category": "resource",
                    "description": "Key team member availability",
                    "probability": "low",
                    "impact": "high",
                    "risk_score": 4,
                    "mitigation": "Cross-training and documentation",
                    "owner": "Project Manager",
                    "status": "mitigating"
                },
                {
                    "id": "RISK-003",
                    "category": "schedule",
                    "description": "External dependency delays",
                    "probability": "medium",
                    "impact": "medium",
                    "risk_score": 5,
                    "mitigation": "Build mock interfaces for parallel development",
                    "owner": "Tech Lead",
                    "status": "mitigating"
                }
            ],
            "risk_summary": {
                "critical": 0,
                "high": 2,
                "medium": 1,
                "low": 0
            },
            "recommendations": [
                "Schedule weekly risk review",
                "Escalate integration risk to steering committee",
                "Accelerate cross-training initiative"
            ],
            "context_analysis": f"Assessment based on: {context}"
        }
        
        return str(assessment)
