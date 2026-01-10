"""
Tasks for the Intake Agent.
"""

from crewai import Task, Agent


class IntakeTasks:
    """Task definitions for the Intake Agent."""
    
    @staticmethod
    def triage_ticket(agent: Agent, ticket_data: str) -> Task:
        """
        Task to triage and classify an incoming ticket.
        
        Args:
            agent: The agent to assign this task to
            ticket_data: The raw ticket information to process
        
        Returns:
            Task: The configured triage task
        """
        return Task(
            description=f"""
            Analyze and triage the following incoming ticket:
            
            {ticket_data}
            
            Your responsibilities:
            1. Parse and understand the ticket content
            2. Classify the ticket type (bug, feature request, enhancement, support, etc.)
            3. Assess priority (critical, high, medium, low) based on impact and urgency
            4. Identify the affected system/component
            5. Tag with relevant labels
            6. Check for potential duplicate tickets
            7. Determine if additional information is needed
            
            Consider factors like:
            - Business impact
            - Number of users affected
            - Workaround availability
            - Security implications
            - Compliance requirements
            """,
            expected_output="""
            A structured triage report containing:
            - Ticket ID and Title
            - Classification (type, priority, severity)
            - Affected Component/System
            - Recommended Labels/Tags
            - Initial Assessment Summary
            - Duplicate Check Results
            - Information Gaps (if any)
            - Recommended Next Steps
            - Suggested Assignee/Team
            """,
            agent=agent,
        )
    
    @staticmethod
    def batch_process_tickets(agent: Agent, tickets: list) -> Task:
        """
        Task to process multiple tickets in batch.
        
        Args:
            agent: The agent to assign this task to
            tickets: List of tickets to process
        
        Returns:
            Task: The configured batch processing task
        """
        tickets_str = "\n---\n".join([str(t) for t in tickets])
        
        return Task(
            description=f"""
            Process the following batch of tickets for initial triage:
            
            {tickets_str}
            
            For each ticket:
            1. Perform quick classification
            2. Assign priority
            3. Identify obvious duplicates within the batch
            4. Group related tickets
            5. Flag any urgent items that need immediate attention
            
            Optimize for efficiency while maintaining accuracy.
            """,
            expected_output="""
            A batch processing report containing:
            - Summary statistics (count by type, priority)
            - List of triaged tickets with classifications
            - Grouped related tickets
            - Identified duplicates
            - Urgent items flagged for immediate attention
            - Recommendations for batch assignment
            """,
            agent=agent,
        )
    
    @staticmethod
    def extract_ticket_requirements(agent: Agent, ticket_data: str) -> Task:
        """
        Task to extract initial requirements from a ticket.
        
        Args:
            agent: The agent to assign this task to
            ticket_data: The ticket to analyze
        
        Returns:
            Task: The configured extraction task
        """
        return Task(
            description=f"""
            Extract initial requirements information from this ticket:
            
            {ticket_data}
            
            Focus on:
            1. Identifying the core problem or need
            2. Extracting any stated requirements
            3. Noting implicit requirements
            4. Identifying stakeholders mentioned
            5. Capturing any constraints or dependencies mentioned
            6. Listing questions that need clarification
            """,
            expected_output="""
            Requirements extraction containing:
            - Problem Statement
            - Explicit Requirements (what was directly stated)
            - Implicit Requirements (inferred needs)
            - Stakeholders Identified
            - Constraints & Dependencies
            - Clarification Questions
            - Preliminary Scope Assessment
            """,
            agent=agent,
        )
    
    @staticmethod
    def identify_duplicates(agent: Agent, new_ticket: str, existing_tickets: str) -> Task:
        """
        Task to identify potential duplicate tickets.
        
        Args:
            agent: The agent to assign this task to
            new_ticket: The new ticket to check
            existing_tickets: Summary of existing tickets to check against
        
        Returns:
            Task: The configured duplicate identification task
        """
        return Task(
            description=f"""
            Check if this new ticket is a duplicate or related to existing tickets:
            
            NEW TICKET:
            {new_ticket}
            
            EXISTING TICKETS:
            {existing_tickets}
            
            Analyze:
            1. Semantic similarity in problem descriptions
            2. Same affected components or features
            3. Similar symptoms or error messages
            4. Related but distinct issues
            5. Potential parent-child relationships
            """,
            expected_output="""
            Duplicate analysis report:
            - Is Duplicate: Yes/No
            - Potential Duplicate Of: [ticket IDs if applicable]
            - Related Tickets: [ticket IDs]
            - Relationship Type (duplicate, related, parent, child)
            - Confidence Level (high, medium, low)
            - Recommendation (merge, link, proceed as new)
            - Reasoning for conclusion
            """,
            agent=agent,
        )
