"""
DevLifecycle Crew - Main crew orchestration module.

This module defines the main Crew class that orchestrates all agents
and their tasks for managing the software development lifecycle.
"""

from typing import Optional, List, Dict, Any
from crewai import Crew, Process

from devlifecycle_crew.agents import (
    IntakeAgent,
    RequirementsAgent,
    SDLCManagerAgent,
    QualityAgent,
    PlanningAgent,
)
from devlifecycle_crew.tasks import (
    IntakeTasks,
    RequirementsTasks,
    SDLCTasks,
    QualityTasks,
    PlanningTasks,
)
from devlifecycle_crew.tools import (
    TicketCreatorTool,
    TicketSearchTool,
    TicketUpdaterTool,
    RequirementsParserTool,
    RequirementsValidatorTool,
    TraceabilityMatrixTool,
    SprintPlannerTool,
    StatusTrackerTool,
    RiskAssessmentTool,
)
from devlifecycle_crew.config.settings import get_settings


class DevLifecycleCrew:
    """
    Main orchestration class for the DevLifecycle agent system.
    
    This crew helps developers manage:
    - Intake tickets (triage, classification, routing)
    - Requirements (analysis, user stories, validation)
    - SDLC processes (planning, tracking, reporting)
    - Quality assurance (testing strategy, risk assessment)
    - Sprint/release planning
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize the DevLifecycle Crew.
        
        Args:
            verbose: Whether to enable verbose output
        """
        self.settings = get_settings()
        self.verbose = verbose
        
        # Initialize tools
        self.ticket_tools = [
            TicketCreatorTool(),
            TicketSearchTool(),
            TicketUpdaterTool(),
        ]
        
        self.requirements_tools = [
            RequirementsParserTool(),
            RequirementsValidatorTool(),
            TraceabilityMatrixTool(),
        ]
        
        self.sdlc_tools = [
            SprintPlannerTool(),
            StatusTrackerTool(),
            RiskAssessmentTool(),
        ]
        
        # Initialize agents
        self._init_agents()
    
    def _init_agents(self):
        """Initialize all agents with their respective tools."""
        self.intake_agent = IntakeAgent.create(
            tools=self.ticket_tools
        )
        
        self.requirements_agent = RequirementsAgent.create(
            tools=self.requirements_tools + self.ticket_tools
        )
        
        self.sdlc_manager_agent = SDLCManagerAgent.create(
            tools=self.sdlc_tools + self.ticket_tools
        )
        
        self.quality_agent = QualityAgent.create(
            tools=self.requirements_tools
        )
        
        self.planning_agent = PlanningAgent.create(
            tools=self.sdlc_tools
        )
    
    def process_ticket(self, ticket_data: str) -> str:
        """
        Process a single incoming ticket through the full intake workflow.
        
        Args:
            ticket_data: Raw ticket information
        
        Returns:
            Processing results from the crew
        """
        # Create tasks for ticket processing
        triage_task = IntakeTasks.triage_ticket(
            self.intake_agent, 
            ticket_data
        )
        
        extract_task = IntakeTasks.extract_ticket_requirements(
            self.intake_agent,
            ticket_data
        )
        
        analyze_task = RequirementsTasks.analyze_requirements(
            self.requirements_agent,
            ticket_data
        )
        
        # Create and run crew
        crew = Crew(
            agents=[self.intake_agent, self.requirements_agent],
            tasks=[triage_task, extract_task, analyze_task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def analyze_requirements(
        self, 
        requirements_text: str,
        create_stories: bool = True,
        validate: bool = True
    ) -> str:
        """
        Analyze requirements and optionally create user stories.
        
        Args:
            requirements_text: Raw requirements text
            create_stories: Whether to create user stories
            validate: Whether to validate requirements
        
        Returns:
            Analysis results
        """
        tasks = []
        agents = [self.requirements_agent]
        
        # Core analysis task
        analyze_task = RequirementsTasks.analyze_requirements(
            self.requirements_agent,
            requirements_text
        )
        tasks.append(analyze_task)
        
        # Optional user story creation
        if create_stories:
            stories_task = RequirementsTasks.create_user_stories(
                self.requirements_agent,
                requirements_text
            )
            tasks.append(stories_task)
        
        # Optional validation with quality agent
        if validate:
            agents.append(self.quality_agent)
            validate_task = RequirementsTasks.validate_requirements(
                self.requirements_agent,
                requirements_text
            )
            tasks.append(validate_task)
            
            testability_task = QualityTasks.review_requirements_testability(
                self.quality_agent,
                requirements_text
            )
            tasks.append(testability_task)
        
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def plan_sprint(
        self,
        backlog: str,
        team_capacity: str,
        sprint_goal: str
    ) -> str:
        """
        Plan a sprint with the available backlog.
        
        Args:
            backlog: Available backlog items
            team_capacity: Team capacity information
            sprint_goal: Desired sprint outcome
        
        Returns:
            Sprint plan
        """
        estimate_task = PlanningTasks.estimate_work(
            self.planning_agent,
            backlog
        )
        
        plan_task = PlanningTasks.plan_sprint(
            self.planning_agent,
            backlog,
            team_capacity,
            sprint_goal
        )
        
        risk_task = QualityTasks.assess_quality_risks(
            self.quality_agent,
            f"Sprint: {sprint_goal}\nBacklog: {backlog}\nCapacity: {team_capacity}"
        )
        
        crew = Crew(
            agents=[self.planning_agent, self.quality_agent],
            tasks=[estimate_task, plan_task, risk_task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def plan_release(
        self,
        features: str,
        constraints: str,
        timeline: str
    ) -> str:
        """
        Plan a release with given features and constraints.
        
        Args:
            features: Features/scope for the release
            constraints: Release constraints
            timeline: Timeline requirements
        
        Returns:
            Release plan
        """
        release_task = PlanningTasks.plan_release(
            self.planning_agent,
            features,
            constraints,
            timeline
        )
        
        project_plan_task = SDLCTasks.create_project_plan(
            self.sdlc_manager_agent,
            features,
            f"Timeline: {timeline}\nConstraints: {constraints}"
        )
        
        crew = Crew(
            agents=[self.planning_agent, self.sdlc_manager_agent],
            tasks=[release_task, project_plan_task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def generate_status_report(self, project_data: str) -> str:
        """
        Generate a comprehensive project status report.
        
        Args:
            project_data: Current project status information
        
        Returns:
            Status report
        """
        status_task = SDLCTasks.generate_status_report(
            self.sdlc_manager_agent,
            project_data
        )
        
        crew = Crew(
            agents=[self.sdlc_manager_agent],
            tasks=[status_task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def assess_change_impact(
        self,
        change_request: str,
        current_state: str
    ) -> str:
        """
        Assess the impact of a proposed change.
        
        Args:
            change_request: The proposed change
            current_state: Current project state
        
        Returns:
            Impact assessment report
        """
        impact_task = SDLCTasks.assess_change_impact(
            self.sdlc_manager_agent,
            change_request,
            current_state
        )
        
        risk_task = QualityTasks.assess_quality_risks(
            self.quality_agent,
            f"Change: {change_request}\nCurrent State: {current_state}"
        )
        
        crew = Crew(
            agents=[self.sdlc_manager_agent, self.quality_agent],
            tasks=[impact_task, risk_task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def create_test_strategy(
        self,
        requirements: str,
        project_context: str
    ) -> str:
        """
        Create a comprehensive test strategy.
        
        Args:
            requirements: Requirements to test
            project_context: Project context information
        
        Returns:
            Test strategy document
        """
        testability_task = QualityTasks.review_requirements_testability(
            self.quality_agent,
            requirements
        )
        
        strategy_task = QualityTasks.create_test_strategy(
            self.quality_agent,
            requirements,
            project_context
        )
        
        crew = Crew(
            agents=[self.quality_agent],
            tasks=[testability_task, strategy_task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def full_ticket_to_sprint_workflow(
        self,
        tickets: List[str],
        team_capacity: str,
        sprint_goal: str
    ) -> str:
        """
        Execute a full workflow from tickets to sprint plan.
        
        This is a comprehensive workflow that:
        1. Triages all tickets
        2. Extracts and analyzes requirements
        3. Creates user stories
        4. Validates requirements
        5. Plans the sprint
        
        Args:
            tickets: List of ticket descriptions
            team_capacity: Team capacity information
            sprint_goal: Sprint goal
        
        Returns:
            Complete workflow results
        """
        tasks = []
        
        # Batch triage
        triage_task = IntakeTasks.batch_process_tickets(
            self.intake_agent,
            tickets
        )
        tasks.append(triage_task)
        
        # Analyze requirements from all tickets
        combined_tickets = "\n---\n".join(tickets)
        analyze_task = RequirementsTasks.analyze_requirements(
            self.requirements_agent,
            combined_tickets
        )
        tasks.append(analyze_task)
        
        # Create user stories
        stories_task = RequirementsTasks.create_user_stories(
            self.requirements_agent,
            combined_tickets
        )
        tasks.append(stories_task)
        
        # Validate requirements
        validate_task = RequirementsTasks.validate_requirements(
            self.requirements_agent,
            combined_tickets
        )
        tasks.append(validate_task)
        
        # Quality review
        testability_task = QualityTasks.review_requirements_testability(
            self.quality_agent,
            combined_tickets
        )
        tasks.append(testability_task)
        
        # Plan sprint
        plan_task = PlanningTasks.plan_sprint(
            self.planning_agent,
            combined_tickets,
            team_capacity,
            sprint_goal
        )
        tasks.append(plan_task)
        
        crew = Crew(
            agents=[
                self.intake_agent,
                self.requirements_agent,
                self.quality_agent,
                self.planning_agent,
            ],
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def manage_blockers(self, blockers: str) -> str:
        """
        Analyze blockers and create resolution plans.
        
        Args:
            blockers: Description of current blockers
        
        Returns:
            Blocker resolution plan
        """
        blocker_task = SDLCTasks.manage_blockers(
            self.sdlc_manager_agent,
            blockers
        )
        
        crew = Crew(
            agents=[self.sdlc_manager_agent],
            tasks=[blocker_task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def quality_gate_check(
        self,
        deliverables: str,
        criteria: str
    ) -> str:
        """
        Perform a quality gate check.
        
        Args:
            deliverables: Deliverables to check
            criteria: Quality criteria to evaluate against
        
        Returns:
            Quality gate assessment
        """
        gate_task = QualityTasks.perform_quality_gate_check(
            self.quality_agent,
            deliverables,
            criteria
        )
        
        crew = Crew(
            agents=[self.quality_agent],
            tasks=[gate_task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def run_custom_workflow(
        self,
        workflow_config: Dict[str, Any]
    ) -> str:
        """
        Run a custom workflow based on configuration.
        
        Args:
            workflow_config: Configuration dictionary specifying:
                - agents: List of agent names to use
                - tasks: List of task configurations
                - process: 'sequential' or 'hierarchical'
        
        Returns:
            Workflow results
        """
        agent_map = {
            "intake": self.intake_agent,
            "requirements": self.requirements_agent,
            "sdlc_manager": self.sdlc_manager_agent,
            "quality": self.quality_agent,
            "planning": self.planning_agent,
        }
        
        agents = [
            agent_map[name] 
            for name in workflow_config.get("agents", ["intake"])
        ]
        
        process = (
            Process.hierarchical 
            if workflow_config.get("process") == "hierarchical"
            else Process.sequential
        )
        
        # Build tasks from config
        tasks = []
        for task_config in workflow_config.get("tasks", []):
            task_type = task_config.get("type")
            agent_name = task_config.get("agent", "intake")
            agent = agent_map[agent_name]
            
            # Map task types to task functions
            if task_type == "triage":
                task = IntakeTasks.triage_ticket(
                    agent, 
                    task_config.get("data", "")
                )
            elif task_type == "analyze_requirements":
                task = RequirementsTasks.analyze_requirements(
                    agent,
                    task_config.get("data", "")
                )
            elif task_type == "create_stories":
                task = RequirementsTasks.create_user_stories(
                    agent,
                    task_config.get("data", "")
                )
            elif task_type == "plan_sprint":
                task = PlanningTasks.plan_sprint(
                    agent,
                    task_config.get("backlog", ""),
                    task_config.get("capacity", ""),
                    task_config.get("goal", "")
                )
            elif task_type == "status_report":
                task = SDLCTasks.generate_status_report(
                    agent,
                    task_config.get("data", "")
                )
            else:
                continue
            
            tasks.append(task)
        
        if not tasks:
            return "No valid tasks configured"
        
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=process,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
