"""
Tasks for the Quality Agent.
"""

from crewai import Task, Agent


class QualityTasks:
    """Task definitions for the Quality Agent."""
    
    @staticmethod
    def review_requirements_testability(agent: Agent, requirements: str) -> Task:
        """
        Task to review requirements for testability.
        
        Args:
            agent: The agent to assign this task to
            requirements: The requirements to review
        
        Returns:
            Task: The configured review task
        """
        return Task(
            description=f"""
            Review the following requirements for testability:
            
            {requirements}
            
            For each requirement, assess:
            1. Is it specific and measurable?
            2. Can it be verified/validated?
            3. Are acceptance criteria clear and testable?
            4. Are there edge cases to consider?
            5. What types of tests are needed? (unit, integration, e2e, etc.)
            6. Are there performance/load testing needs?
            7. Security testing requirements?
            8. Accessibility testing needs?
            
            Flag any requirements that are untestable and suggest improvements.
            """,
            expected_output="""
            Testability Review Report:
            
            1. OVERALL TESTABILITY SCORE
               - Score: [X/10]
               - Summary assessment
            
            2. REQUIREMENT-BY-REQUIREMENT ANALYSIS
               For each requirement:
               - Requirement ID
               - Testability: [High/Medium/Low/Not Testable]
               - Issues Found
               - Suggested Improvements
               - Test Types Needed
               - Estimated Test Effort
            
            3. TEST STRATEGY RECOMMENDATIONS
               - Unit Testing Needs
               - Integration Testing Needs
               - End-to-End Testing Needs
               - Performance Testing Needs
               - Security Testing Needs
               - Accessibility Testing Needs
            
            4. UNTESTABLE REQUIREMENTS
               - List with reasons
               - Recommended rewrites
            
            5. EDGE CASES IDENTIFIED
               - Requirement
               - Edge case description
               - Test scenario needed
            
            6. TEST ENVIRONMENT REQUIREMENTS
               - Special environments needed
               - Data requirements
               - Tools needed
            """,
            agent=agent,
        )
    
    @staticmethod
    def create_test_strategy(agent: Agent, requirements: str, project_context: str) -> Task:
        """
        Task to create a comprehensive test strategy.
        
        Args:
            agent: The agent to assign this task to
            requirements: The requirements to test
            project_context: Project information for context
        
        Returns:
            Task: The configured test strategy task
        """
        return Task(
            description=f"""
            Create a comprehensive test strategy for:
            
            REQUIREMENTS:
            {requirements}
            
            PROJECT CONTEXT:
            {project_context}
            
            The strategy should cover:
            1. Test objectives and scope
            2. Test levels (unit, integration, system, acceptance)
            3. Test types (functional, performance, security, etc.)
            4. Entry and exit criteria
            5. Test environment requirements
            6. Test data requirements
            7. Tools and automation approach
            8. Resource and timeline estimates
            9. Risk-based testing priorities
            10. Defect management process
            """,
            expected_output="""
            Test Strategy Document:
            
            1. OVERVIEW
               - Test Objectives
               - Scope (In/Out)
               - Key Stakeholders
            
            2. TEST APPROACH
               - Testing Methodology
               - Test Levels and Types
               
               | Level | Type | Description | Tools |
               |-------|------|-------------|-------|
            
            3. TEST COVERAGE
               - Coverage Goals
               - Priority Areas
               - Risk-Based Priorities
            
            4. TEST ENVIRONMENT
               - Environment Requirements
               - Data Requirements
               - Setup/Teardown Procedures
            
            5. AUTOMATION STRATEGY
               - What to Automate
               - Tools/Frameworks
               - Automation Coverage Goals
            
            6. ENTRY/EXIT CRITERIA
               - Entry Criteria for Each Level
               - Exit Criteria for Each Level
               - Release Criteria
            
            7. DEFECT MANAGEMENT
               - Defect Lifecycle
               - Severity Definitions
               - Priority Definitions
               - SLA Targets
            
            8. SCHEDULE & RESOURCES
               - Timeline
               - Resource Requirements
               - Dependencies
            
            9. RISKS & MITIGATIONS
               - Testing Risks
               - Mitigation Plans
            
            10. METRICS & REPORTING
                - Key Metrics
                - Reporting Frequency
                - Dashboard Requirements
            """,
            agent=agent,
        )
    
    @staticmethod
    def assess_quality_risks(agent: Agent, project_data: str) -> Task:
        """
        Task to assess quality risks.
        
        Args:
            agent: The agent to assign this task to
            project_data: Current project information
        
        Returns:
            Task: The configured risk assessment task
        """
        return Task(
            description=f"""
            Assess quality risks for the project:
            
            {project_data}
            
            Identify and analyze risks related to:
            1. Technical complexity
            2. Requirement clarity
            3. Timeline pressure
            4. Resource constraints
            5. Integration challenges
            6. Third-party dependencies
            7. Testing coverage gaps
            8. Performance concerns
            9. Security vulnerabilities
            10. Technical debt
            
            Provide risk ratings and mitigation strategies.
            """,
            expected_output="""
            Quality Risk Assessment:
            
            1. RISK SUMMARY
               - Overall Risk Level: [High/Medium/Low]
               - Critical Risks: [count]
               - High Risks: [count]
               - Medium/Low Risks: [count]
            
            2. RISK REGISTER
               For each risk:
               - Risk ID
               - Category
               - Description
               - Probability: [High/Medium/Low]
               - Impact: [High/Medium/Low]
               - Risk Score
               - Mitigation Strategy
               - Contingency Plan
               - Owner
               - Status
            
            3. TOP RISKS
               - Top 5 risks requiring immediate attention
               - Recommended actions
            
            4. RISK TRENDS
               - New risks identified
               - Risks increasing
               - Risks decreasing
            
            5. RECOMMENDATIONS
               - Priority actions
               - Resource needs
               - Escalations needed
            """,
            agent=agent,
        )
    
    @staticmethod
    def generate_quality_metrics(agent: Agent, test_results: str, defect_data: str) -> Task:
        """
        Task to generate quality metrics report.
        
        Args:
            agent: The agent to assign this task to
            test_results: Test execution results
            defect_data: Defect information
        
        Returns:
            Task: The configured metrics task
        """
        return Task(
            description=f"""
            Generate a quality metrics report based on:
            
            TEST RESULTS:
            {test_results}
            
            DEFECT DATA:
            {defect_data}
            
            Calculate and report on:
            1. Test execution metrics (pass/fail/blocked rates)
            2. Test coverage metrics
            3. Defect metrics (density, severity distribution)
            4. Defect discovery and fix rates
            5. Defect age analysis
            6. Test efficiency metrics
            7. Quality trends over time
            8. Release readiness indicators
            """,
            expected_output="""
            Quality Metrics Report:
            
            1. EXECUTIVE SUMMARY
               - Quality Status: [Good/Fair/Poor]
               - Key Highlights
               - Areas of Concern
            
            2. TEST EXECUTION METRICS
               - Total Tests: X
               - Passed: X (X%)
               - Failed: X (X%)
               - Blocked: X (X%)
               - Not Run: X (X%)
               - Pass Rate Trend
            
            3. COVERAGE METRICS
               - Requirements Coverage: X%
               - Code Coverage: X%
               - Risk Coverage: X%
            
            4. DEFECT METRICS
               - Total Defects: X
               - By Severity: Critical(X), High(X), Medium(X), Low(X)
               - By Status: Open(X), Fixed(X), Verified(X), Closed(X)
               - Defect Density: X defects per KLOC
               - Discovery Rate: X/day
               - Fix Rate: X/day
               - Average Age: X days
            
            5. TRENDS
               - Defect discovery trend (chart)
               - Fix rate trend (chart)
               - Pass rate trend (chart)
            
            6. RELEASE READINESS
               - Criteria Assessment
               - Go/No-Go Indicators
               - Outstanding Issues
            
            7. RECOMMENDATIONS
               - Quality Improvements
               - Process Improvements
               - Risk Mitigations
            """,
            agent=agent,
        )
    
    @staticmethod
    def perform_quality_gate_check(agent: Agent, deliverables: str, criteria: str) -> Task:
        """
        Task to perform quality gate verification.
        
        Args:
            agent: The agent to assign this task to
            deliverables: The deliverables to check
            criteria: Quality gate criteria
        
        Returns:
            Task: The configured quality gate task
        """
        return Task(
            description=f"""
            Perform quality gate verification:
            
            DELIVERABLES:
            {deliverables}
            
            QUALITY CRITERIA:
            {criteria}
            
            Verify:
            1. All mandatory criteria are met
            2. Documentation is complete
            3. Test coverage thresholds are met
            4. No critical or high severity defects open
            5. Performance benchmarks met
            6. Security scan passed
            7. Code review completed
            8. Stakeholder approvals obtained
            
            Provide pass/fail determination with detailed rationale.
            """,
            expected_output="""
            Quality Gate Assessment:
            
            1. GATE RESULT
               - Status: [PASS / FAIL / CONDITIONAL PASS]
               - Assessment Date
               - Assessor
            
            2. CRITERIA CHECKLIST
               | Criterion | Required | Actual | Status |
               |-----------|----------|--------|--------|
               | Test Coverage | X% | Y% | ✓/✗ |
               | Critical Defects | 0 | Y | ✓/✗ |
               | ...
            
            3. DETAILED FINDINGS
               - Criteria met
               - Criteria not met
               - Exceptions granted
            
            4. OUTSTANDING ITEMS
               - Items requiring attention
               - Remediation timeline
            
            5. WAIVERS/EXCEPTIONS
               - Criteria waived
               - Justification
               - Approver
            
            6. RECOMMENDATION
               - Proceed / Do Not Proceed / Proceed with Conditions
               - Conditions (if any)
               - Risk acceptance (if any)
            
            7. SIGN-OFF
               - Required approvals
               - Approval status
            """,
            agent=agent,
        )
