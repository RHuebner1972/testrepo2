"""
Tasks for the Requirements Agent.
"""

from crewai import Task, Agent


class RequirementsTasks:
    """Task definitions for the Requirements Agent."""
    
    @staticmethod
    def analyze_requirements(agent: Agent, ticket_data: str, context: str = "") -> Task:
        """
        Task to perform detailed requirements analysis.
        
        Args:
            agent: The agent to assign this task to
            ticket_data: The ticket/request to analyze
            context: Additional context information
        
        Returns:
            Task: The configured analysis task
        """
        return Task(
            description=f"""
            Perform comprehensive requirements analysis on the following:
            
            TICKET/REQUEST:
            {ticket_data}
            
            ADDITIONAL CONTEXT:
            {context if context else "None provided"}
            
            Your analysis should:
            1. Identify all functional requirements
            2. Identify non-functional requirements (performance, security, etc.)
            3. Define clear acceptance criteria
            4. Identify assumptions being made
            5. List dependencies on other systems or features
            6. Identify potential risks or concerns
            7. Note any ambiguities that need clarification
            8. Suggest requirement priority (must-have, should-have, nice-to-have)
            
            Use industry best practices for requirements documentation.
            """,
            expected_output="""
            Comprehensive Requirements Document containing:
            
            1. OVERVIEW
               - Summary
               - Business Value
               - Stakeholders
            
            2. FUNCTIONAL REQUIREMENTS
               - Numbered list with clear, testable statements
               - Each with priority and rationale
            
            3. NON-FUNCTIONAL REQUIREMENTS
               - Performance requirements
               - Security requirements
               - Scalability requirements
               - Usability requirements
            
            4. ACCEPTANCE CRITERIA
               - Given/When/Then format
               - Clear pass/fail conditions
            
            5. ASSUMPTIONS & CONSTRAINTS
            
            6. DEPENDENCIES
            
            7. RISKS & CONCERNS
            
            8. OPEN QUESTIONS
            
            9. OUT OF SCOPE (explicitly excluded)
            """,
            agent=agent,
        )
    
    @staticmethod
    def create_user_stories(agent: Agent, requirements: str) -> Task:
        """
        Task to create user stories from requirements.
        
        Args:
            agent: The agent to assign this task to
            requirements: The requirements to convert
        
        Returns:
            Task: The configured user story creation task
        """
        return Task(
            description=f"""
            Create well-structured user stories from these requirements:
            
            {requirements}
            
            For each user story:
            1. Use the format: "As a [user type], I want [goal] so that [benefit]"
            2. Keep stories small and focused (should be completable in one sprint)
            3. Write clear acceptance criteria using Given/When/Then
            4. Identify the user persona appropriately
            5. Ensure stories are independent where possible
            6. Estimate relative complexity (story points: 1, 2, 3, 5, 8, 13)
            
            Follow INVEST principles:
            - Independent
            - Negotiable
            - Valuable
            - Estimable
            - Small
            - Testable
            """,
            expected_output="""
            User Story Document containing:
            
            For each story:
            - Story ID
            - Title
            - User Story Statement
            - Acceptance Criteria (Given/When/Then)
            - Story Points Estimate
            - Dependencies (on other stories)
            - Notes/Assumptions
            
            Summary:
            - Total story count
            - Total story points
            - Suggested story sequence/priority
            """,
            agent=agent,
        )
    
    @staticmethod
    def validate_requirements(agent: Agent, requirements: str) -> Task:
        """
        Task to validate requirements for quality and completeness.
        
        Args:
            agent: The agent to assign this task to
            requirements: The requirements to validate
        
        Returns:
            Task: The configured validation task
        """
        return Task(
            description=f"""
            Validate the following requirements for quality and completeness:
            
            {requirements}
            
            Check for:
            1. Completeness - Are all necessary details included?
            2. Consistency - Do requirements contradict each other?
            3. Clarity - Is each requirement unambiguous?
            4. Testability - Can each requirement be verified?
            5. Feasibility - Are requirements technically achievable?
            6. Traceability - Can requirements be traced to business needs?
            7. Priority - Are priorities clearly defined?
            8. Dependencies - Are all dependencies identified?
            
            Identify any issues and provide recommendations for improvement.
            """,
            expected_output="""
            Requirements Validation Report:
            
            1. QUALITY SCORECARD
               - Completeness: [score/5]
               - Consistency: [score/5]
               - Clarity: [score/5]
               - Testability: [score/5]
               - Overall Quality: [score/5]
            
            2. ISSUES FOUND
               - Critical Issues (must fix)
               - Major Issues (should fix)
               - Minor Issues (nice to fix)
            
            3. SPECIFIC RECOMMENDATIONS
               - For each issue, provide specific fix
            
            4. MISSING ELEMENTS
               - List what needs to be added
            
            5. CONFLICTS DETECTED
               - Requirements that contradict
            
            6. APPROVAL RECOMMENDATION
               - Ready for development: Yes/No
               - Conditions for approval
            """,
            agent=agent,
        )
    
    @staticmethod
    def create_traceability_matrix(agent: Agent, requirements: str, artifacts: str) -> Task:
        """
        Task to create a requirements traceability matrix.
        
        Args:
            agent: The agent to assign this task to
            requirements: The requirements to trace
            artifacts: Related artifacts (stories, tests, etc.)
        
        Returns:
            Task: The configured traceability task
        """
        return Task(
            description=f"""
            Create a requirements traceability matrix:
            
            REQUIREMENTS:
            {requirements}
            
            RELATED ARTIFACTS:
            {artifacts}
            
            Build a traceability matrix that:
            1. Links each requirement to its source (business need/ticket)
            2. Links requirements to user stories
            3. Links requirements to test cases (if available)
            4. Identifies gaps in coverage
            5. Shows requirement status
            """,
            expected_output="""
            Requirements Traceability Matrix:
            
            | Req ID | Source | User Stories | Test Cases | Status |
            |--------|--------|--------------|------------|--------|
            | ... | ... | ... | ... | ... |
            
            Coverage Analysis:
            - Requirements with full traceability: X%
            - Requirements missing stories: [list]
            - Requirements missing tests: [list]
            - Orphaned artifacts: [list]
            
            Recommendations for improving traceability
            """,
            agent=agent,
        )
    
    @staticmethod
    def refine_requirements(agent: Agent, requirements: str, feedback: str) -> Task:
        """
        Task to refine requirements based on feedback.
        
        Args:
            agent: The agent to assign this task to
            requirements: The original requirements
            feedback: Feedback received
        
        Returns:
            Task: The configured refinement task
        """
        return Task(
            description=f"""
            Refine the following requirements based on feedback received:
            
            ORIGINAL REQUIREMENTS:
            {requirements}
            
            FEEDBACK:
            {feedback}
            
            Tasks:
            1. Address each piece of feedback
            2. Clarify ambiguous requirements
            3. Add missing details
            4. Resolve conflicts
            5. Update acceptance criteria
            6. Document changes made
            """,
            expected_output="""
            Refined Requirements Document:
            
            1. UPDATED REQUIREMENTS
               - Full updated requirements with changes highlighted
            
            2. CHANGE LOG
               - What changed and why
               - Feedback item addressed
            
            3. REMAINING OPEN ITEMS
               - Questions still needing answers
               - Decisions still pending
            
            4. IMPACT ANALYSIS
               - How changes affect scope
               - How changes affect timeline estimates
            """,
            agent=agent,
        )
