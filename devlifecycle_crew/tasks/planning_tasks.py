"""
Tasks for the Planning Agent.
"""

from crewai import Task, Agent


class PlanningTasks:
    """Task definitions for the Planning Agent."""
    
    @staticmethod
    def estimate_work(agent: Agent, work_items: str, historical_data: str = "") -> Task:
        """
        Task to estimate effort for work items.
        
        Args:
            agent: The agent to assign this task to
            work_items: Items to estimate
            historical_data: Past data for reference
        
        Returns:
            Task: The configured estimation task
        """
        return Task(
            description=f"""
            Estimate effort for the following work items:
            
            WORK ITEMS:
            {work_items}
            
            HISTORICAL DATA:
            {historical_data if historical_data else "None provided"}
            
            For each item:
            1. Assess complexity (Low/Medium/High)
            2. Identify technical challenges
            3. Consider dependencies
            4. Estimate in story points (Fibonacci: 1, 2, 3, 5, 8, 13, 21)
            5. Identify uncertainty factors
            6. Provide confidence level
            7. Note assumptions
            
            Use relative sizing based on similar past work when available.
            """,
            expected_output="""
            Estimation Report:
            
            1. ESTIMATION SUMMARY
               - Total Items: X
               - Total Story Points: X
               - Average Confidence: X%
            
            2. ITEM-BY-ITEM ESTIMATES
               For each item:
               - Item ID/Title
               - Story Points: X
               - Complexity: [Low/Medium/High]
               - Confidence: X%
               - Key Assumptions
               - Risks/Uncertainties
               - Dependencies
               - Notes
            
            3. ESTIMATION BREAKDOWN
               | Points | Count | Total |
               |--------|-------|-------|
               | 1      | X     | X     |
               | 2      | X     | X     |
               | ...    | ...   | ...   |
            
            4. HIGH UNCERTAINTY ITEMS
               - Items needing spike/research
               - Recommended approach
            
            5. RECOMMENDATIONS
               - Items to split
               - Items needing clarification
               - Dependencies to resolve first
            """,
            agent=agent,
        )
    
    @staticmethod
    def plan_sprint(agent: Agent, backlog: str, team_capacity: str, sprint_goal: str) -> Task:
        """
        Task to plan a sprint.
        
        Args:
            agent: The agent to assign this task to
            backlog: Available backlog items
            team_capacity: Team availability information
            sprint_goal: Desired sprint outcome
        
        Returns:
            Task: The configured sprint planning task
        """
        return Task(
            description=f"""
            Plan a sprint with the following inputs:
            
            SPRINT GOAL:
            {sprint_goal}
            
            TEAM CAPACITY:
            {team_capacity}
            
            AVAILABLE BACKLOG:
            {backlog}
            
            Create a sprint plan that:
            1. Aligns with the sprint goal
            2. Respects team capacity (leave buffer for unknowns)
            3. Prioritizes by business value
            4. Considers dependencies
            5. Balances work across team members
            6. Includes time for meetings, reviews, etc.
            7. Aims for 80-85% capacity utilization
            8. Groups related items when possible
            """,
            expected_output="""
            Sprint Plan:
            
            1. SPRINT OVERVIEW
               - Sprint Number/Name
               - Duration
               - Sprint Goal
               - Start/End Dates
            
            2. CAPACITY PLANNING
               - Total Capacity: X story points / X hours
               - Planned Load: X story points / X hours
               - Buffer: X%
               - Utilization: X%
            
            3. COMMITTED ITEMS
               | Priority | ID | Title | Points | Assignee |
               |----------|-----|-------|--------|----------|
               | 1        | ... | ...   | ...    | ...      |
            
            4. SPRINT BACKLOG
               - Total Items: X
               - Total Points: X
               - By Type: Features(X), Bugs(X), Tech Debt(X)
            
            5. DEPENDENCIES
               - Internal dependencies (within sprint)
               - External dependencies (outside team)
            
            6. RISKS
               - Identified risks to sprint success
               - Mitigation plans
            
            7. NOT INCLUDED
               - Items considered but not included
               - Reason for exclusion
            
            8. SUCCESS CRITERIA
               - Definition of Done
               - Sprint success measures
            """,
            agent=agent,
        )
    
    @staticmethod
    def plan_release(agent: Agent, features: str, constraints: str, timeline: str) -> Task:
        """
        Task to plan a release.
        
        Args:
            agent: The agent to assign this task to
            features: Features for the release
            constraints: Release constraints
            timeline: Timeline requirements
        
        Returns:
            Task: The configured release planning task
        """
        return Task(
            description=f"""
            Plan a release with the following:
            
            FEATURES/SCOPE:
            {features}
            
            CONSTRAINTS:
            {constraints}
            
            TIMELINE:
            {timeline}
            
            Create a release plan that:
            1. Sequences features appropriately
            2. Identifies release milestones
            3. Plans for multiple sprints/iterations
            4. Accounts for hardening/stabilization
            5. Includes deployment planning
            6. Defines rollback strategy
            7. Plans communication/documentation
            8. Identifies go/no-go criteria
            """,
            expected_output="""
            Release Plan:
            
            1. RELEASE OVERVIEW
               - Release Name/Version
               - Release Date
               - Release Theme/Goals
               - Key Features
            
            2. SCOPE
               - In Scope (must-have)
               - In Scope (should-have)
               - Out of Scope (deferred)
            
            3. RELEASE TIMELINE
               - Sprint/Iteration Breakdown
               - Key Milestones
               - Code Freeze Date
               - Release Date
               
               | Phase | Start | End | Activities |
               |-------|-------|-----|------------|
            
            4. FEATURE SEQUENCE
               - Delivery order
               - Dependencies
               - MVP definition
            
            5. RELEASE CRITERIA
               - Quality Gates
               - Go/No-Go Criteria
               - Sign-off Requirements
            
            6. DEPLOYMENT PLAN
               - Environment Strategy
               - Deployment Sequence
               - Rollback Plan
            
            7. COMMUNICATION PLAN
               - Internal Communication
               - External Communication
               - Documentation Updates
            
            8. RISKS & DEPENDENCIES
               - Release Risks
               - External Dependencies
               - Mitigation Plans
            
            9. SUCCESS METRICS
               - How success will be measured
               - KPIs to track
            """,
            agent=agent,
        )
    
    @staticmethod
    def optimize_backlog(agent: Agent, backlog: str, priorities: str) -> Task:
        """
        Task to optimize and prioritize the backlog.
        
        Args:
            agent: The agent to assign this task to
            backlog: Current backlog items
            priorities: Business priorities
        
        Returns:
            Task: The configured backlog optimization task
        """
        return Task(
            description=f"""
            Optimize and prioritize the backlog:
            
            CURRENT BACKLOG:
            {backlog}
            
            BUSINESS PRIORITIES:
            {priorities}
            
            Tasks:
            1. Apply prioritization framework (WSJF, MoSCoW, etc.)
            2. Identify quick wins (high value, low effort)
            3. Group related items
            4. Identify items to split
            5. Flag items needing refinement
            6. Recommend items to remove/defer
            7. Ensure alignment with business goals
            """,
            expected_output="""
            Backlog Optimization Report:
            
            1. PRIORITIZED BACKLOG
               | Rank | ID | Title | Value | Effort | Priority Score |
               |------|-----|-------|-------|--------|----------------|
            
            2. QUICK WINS
               - High value, low effort items
               - Recommended for immediate action
            
            3. GROUPINGS
               - Related items that should be done together
               - Suggested epic/theme structure
            
            4. ITEMS TO SPLIT
               - Large items needing breakdown
               - Suggested split approach
            
            5. NEEDS REFINEMENT
               - Items lacking clarity
               - Specific questions to address
            
            6. RECOMMENDED REMOVALS
               - Items to remove/archive
               - Reason for removal
            
            7. DEFERRALS
               - Items to defer
               - Suggested timeline
            
            8. ALIGNMENT CHECK
               - How backlog aligns with business goals
               - Gaps identified
               - Recommendations
            """,
            agent=agent,
        )
    
    @staticmethod
    def replan_sprint(agent: Agent, current_sprint: str, changes: str) -> Task:
        """
        Task to replan a sprint mid-flight.
        
        Args:
            agent: The agent to assign this task to
            current_sprint: Current sprint status
            changes: Changes requiring replan
        
        Returns:
            Task: The configured replanning task
        """
        return Task(
            description=f"""
            Replan the current sprint based on changes:
            
            CURRENT SPRINT STATUS:
            {current_sprint}
            
            CHANGES REQUIRING REPLAN:
            {changes}
            
            Tasks:
            1. Assess impact of changes on sprint
            2. Determine what can be completed
            3. Identify items to remove/defer
            4. Reprioritize remaining work
            5. Communicate changes to stakeholders
            6. Adjust sprint goal if needed
            7. Document lessons learned
            """,
            expected_output="""
            Sprint Replan:
            
            1. REPLAN SUMMARY
               - Reason for Replan
               - Impact Assessment
               - Revised Sprint Goal (if changed)
            
            2. ORIGINAL VS REVISED
               | Metric | Original | Revised | Delta |
               |--------|----------|---------|-------|
               | Story Points | X | Y | -Z |
               | Items | X | Y | -Z |
            
            3. ITEMS AFFECTED
               - Continuing as planned
               - Modified scope/timeline
               - Removed from sprint
               - Added to sprint
            
            4. REVISED SPRINT PLAN
               - Updated item list with new priorities
               - New timeline
               - Resource adjustments
            
            5. DEPENDENCIES IMPACTED
               - Downstream impacts
               - Mitigation actions
            
            6. STAKEHOLDER COMMUNICATION
               - Who needs to know
               - Key messages
               - Timeline for communication
            
            7. LESSONS LEARNED
               - What caused the need to replan
               - Prevention for future
            """,
            agent=agent,
        )
