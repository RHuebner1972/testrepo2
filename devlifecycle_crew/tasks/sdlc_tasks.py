"""
Tasks for the SDLC Manager Agent.
"""

from crewai import Task, Agent


class SDLCTasks:
    """Task definitions for the SDLC Manager Agent."""
    
    @staticmethod
    def create_project_plan(agent: Agent, requirements: str, constraints: str = "") -> Task:
        """
        Task to create a project plan from requirements.
        
        Args:
            agent: The agent to assign this task to
            requirements: The requirements to plan for
            constraints: Any constraints (timeline, resources, etc.)
        
        Returns:
            Task: The configured planning task
        """
        return Task(
            description=f"""
            Create a comprehensive project plan for the following:
            
            REQUIREMENTS:
            {requirements}
            
            CONSTRAINTS:
            {constraints if constraints else "None specified"}
            
            Your plan should include:
            1. Project phases and milestones
            2. High-level timeline estimates
            3. Resource requirements
            4. Key deliverables per phase
            5. Dependencies between phases
            6. Risk assessment
            7. Success criteria
            8. Communication plan
            
            Consider standard SDLC phases:
            - Planning & Analysis
            - Design
            - Development
            - Testing
            - Deployment
            - Maintenance
            """,
            expected_output="""
            Project Plan Document:
            
            1. EXECUTIVE SUMMARY
               - Project overview
               - Key objectives
               - Success criteria
            
            2. PROJECT PHASES
               For each phase:
               - Phase name
               - Duration estimate
               - Key activities
               - Deliverables
               - Exit criteria
            
            3. TIMELINE
               - Gantt chart representation (text format)
               - Key milestones with dates
               - Dependencies
            
            4. RESOURCE PLAN
               - Team composition needed
               - Skills required
               - Allocation percentages
            
            5. RISK ASSESSMENT
               - Identified risks
               - Mitigation strategies
               - Contingency plans
            
            6. COMMUNICATION PLAN
               - Stakeholder updates
               - Team meetings
               - Reporting cadence
            """,
            agent=agent,
        )
    
    @staticmethod
    def generate_status_report(agent: Agent, project_data: str) -> Task:
        """
        Task to generate a project status report.
        
        Args:
            agent: The agent to assign this task to
            project_data: Current project status information
        
        Returns:
            Task: The configured status report task
        """
        return Task(
            description=f"""
            Generate a comprehensive project status report based on:
            
            {project_data}
            
            Include:
            1. Overall project health (on track, at risk, behind)
            2. Progress against milestones
            3. Completed items this period
            4. Items in progress
            5. Blockers and issues
            6. Risks and mitigation status
            7. Key metrics (velocity, burn rate, etc.)
            8. Upcoming priorities
            9. Decisions needed
            """,
            expected_output="""
            Project Status Report:
            
            1. STATUS SUMMARY
               - Overall Status: [🟢 On Track / 🟡 At Risk / 🔴 Behind]
               - Reporting Period
               - Key Highlights
            
            2. MILESTONE PROGRESS
               | Milestone | Target Date | Status | % Complete |
            
            3. SPRINT/ITERATION STATUS
               - Sprint goal
               - Committed vs completed
               - Velocity
            
            4. ACCOMPLISHMENTS
               - Completed items with impact
            
            5. IN PROGRESS
               - Current work items
               - Expected completion
            
            6. BLOCKERS & ISSUES
               - Description
               - Impact
               - Owner
               - Resolution plan
            
            7. RISKS
               - Risk description
               - Probability/Impact
               - Mitigation status
            
            8. METRICS
               - Key performance indicators
               - Trends
            
            9. NEXT PERIOD PRIORITIES
            
            10. DECISIONS NEEDED
                - Decision required
                - Options
                - Recommendation
                - Decision maker
            """,
            agent=agent,
        )
    
    @staticmethod
    def assess_change_impact(agent: Agent, change_request: str, current_state: str) -> Task:
        """
        Task to assess impact of a proposed change.
        
        Args:
            agent: The agent to assign this task to
            change_request: The proposed change
            current_state: Current project state
        
        Returns:
            Task: The configured impact assessment task
        """
        return Task(
            description=f"""
            Assess the impact of this change request:
            
            CHANGE REQUEST:
            {change_request}
            
            CURRENT PROJECT STATE:
            {current_state}
            
            Analyze:
            1. Scope impact - What's affected?
            2. Timeline impact - How does this affect delivery?
            3. Resource impact - Additional effort needed?
            4. Cost impact - Budget implications?
            5. Risk impact - New risks introduced?
            6. Quality impact - Testing implications?
            7. Dependencies - What else is affected?
            
            Provide recommendation on whether to accept, defer, or reject.
            """,
            expected_output="""
            Change Impact Assessment:
            
            1. CHANGE SUMMARY
               - Change ID
               - Description
               - Requestor
               - Reason/Business Need
            
            2. IMPACT ANALYSIS
               - Scope: [High/Medium/Low] - Details
               - Timeline: [+X days/weeks] - Details
               - Resources: [Additional effort] - Details
               - Cost: [Budget impact] - Details
               - Risk: [New risks] - Details
               - Quality: [Testing needs] - Details
            
            3. AFFECTED ITEMS
               - Requirements impacted
               - Stories/tasks affected
               - Dependencies triggered
            
            4. EFFORT ESTIMATE
               - Development effort
               - Testing effort
               - Total additional effort
            
            5. OPTIONS
               - Option A: Accept as-is
               - Option B: Modified approach
               - Option C: Defer to future release
               - Option D: Reject
            
            6. RECOMMENDATION
               - Recommended option
               - Rationale
               - Conditions
            
            7. APPROVAL REQUIREMENTS
               - Who needs to approve
               - Deadline for decision
            """,
            agent=agent,
        )
    
    @staticmethod
    def manage_blockers(agent: Agent, blockers: str) -> Task:
        """
        Task to analyze and provide resolution strategies for blockers.
        
        Args:
            agent: The agent to assign this task to
            blockers: List of current blockers
        
        Returns:
            Task: The configured blocker management task
        """
        return Task(
            description=f"""
            Analyze and develop resolution strategies for these blockers:
            
            {blockers}
            
            For each blocker:
            1. Assess severity and impact
            2. Identify root cause
            3. Determine dependencies on resolution
            4. Propose resolution options
            5. Identify owner and timeline
            6. Suggest escalation path if needed
            """,
            expected_output="""
            Blocker Resolution Plan:
            
            For each blocker:
            
            BLOCKER #[N]
            - Description
            - Severity: [Critical/High/Medium/Low]
            - Items Blocked: [list]
            - Root Cause Analysis
            - Resolution Options:
              1. [Option with pros/cons]
              2. [Option with pros/cons]
            - Recommended Action
            - Owner
            - Target Resolution Date
            - Escalation Path (if needed)
            
            SUMMARY
            - Total blockers: X
            - Critical blockers: X
            - Estimated resolution timeline
            - Executive attention needed: [Yes/No]
            """,
            agent=agent,
        )
    
    @staticmethod
    def coordinate_phase_transition(
        agent: Agent, 
        current_phase: str, 
        next_phase: str, 
        phase_data: str
    ) -> Task:
        """
        Task to coordinate transition between SDLC phases.
        
        Args:
            agent: The agent to assign this task to
            current_phase: The phase being completed
            next_phase: The phase being entered
            phase_data: Relevant phase information
        
        Returns:
            Task: The configured phase transition task
        """
        return Task(
            description=f"""
            Coordinate the transition from {current_phase} to {next_phase}:
            
            PHASE DATA:
            {phase_data}
            
            Tasks:
            1. Verify exit criteria for {current_phase} are met
            2. Confirm entry criteria for {next_phase} are satisfied
            3. Ensure all handoff documentation is complete
            4. Identify any gaps or incomplete items
            5. Confirm resource readiness for next phase
            6. Update project status and stakeholders
            7. Archive current phase artifacts
            """,
            expected_output="""
            Phase Transition Report:
            
            1. PHASE COMPLETION ASSESSMENT
               - Phase: {current_phase}
               - Exit Criteria Checklist:
                 ✓/✗ [Criterion 1]
                 ✓/✗ [Criterion 2]
                 ...
               - Completion Status: [Complete/Incomplete]
            
            2. NEXT PHASE READINESS
               - Phase: {next_phase}
               - Entry Criteria Checklist:
                 ✓/✗ [Criterion 1]
                 ✓/✗ [Criterion 2]
                 ...
               - Readiness Status: [Ready/Not Ready]
            
            3. HANDOFF ITEMS
               - Documents prepared
               - Knowledge transfer completed
               - Outstanding items
            
            4. GAPS IDENTIFIED
               - Gap description
               - Impact
               - Remediation plan
            
            5. RESOURCE STATUS
               - Team readiness
               - Tool/environment readiness
            
            6. GO/NO-GO RECOMMENDATION
               - Recommendation: [Proceed/Hold]
               - Conditions
               - Risks
            
            7. COMMUNICATION
               - Stakeholders notified
               - Key messages
            """,
            agent=agent,
        )
