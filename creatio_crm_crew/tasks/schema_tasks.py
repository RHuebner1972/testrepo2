"""
Tasks for schema analysis in Creatio CRM.
"""

from crewai import Task, Agent


class SchemaAnalysisTasks:
    """Task definitions for schema analysis."""
    
    @staticmethod
    def explore_entity(agent: Agent, entity_name: str) -> Task:
        """
        Task to explore a specific Creatio entity's schema.
        
        Args:
            agent: The agent to assign this task to
            entity_name: Name of the entity to explore
        
        Returns:
            Task: The configured exploration task
        """
        return Task(
            description=f"""
            Thoroughly explore and analyze the schema for the Creatio CRM entity: {entity_name}
            
            Your analysis should include:
            1. Entity description and business purpose
            2. Table name and physical structure
            3. All key columns with their data types and purposes
            4. Foreign key relationships to other entities
            5. Common use cases for this entity
            6. Best practices for querying this entity
            7. Related lookup tables and their purposes
            
            Use your schema exploration tools to gather comprehensive information.
            Present findings in a clear, organized format that would be useful
            for data architects and developers working with this entity.
            """,
            expected_output="""
            A comprehensive entity analysis report containing:
            - Entity Overview (name, purpose, table)
            - Column Catalog (name, type, description, constraints)
            - Relationship Map (related entities, relationship types)
            - Usage Patterns (common queries, joins)
            - Data Architecture Recommendations
            - Sample Queries for common operations
            """,
            agent=agent,
        )
    
    @staticmethod
    def analyze_relationships(
        agent: Agent, 
        source_entity: str, 
        target_entity: str = None
    ) -> Task:
        """
        Task to analyze relationships between entities.
        
        Args:
            agent: The agent to assign this task to
            source_entity: Primary entity to analyze
            target_entity: Optional specific target entity
        
        Returns:
            Task: The configured relationship analysis task
        """
        target_clause = f"and {target_entity}" if target_entity else "and all related entities"
        
        return Task(
            description=f"""
            Analyze the relationships between {source_entity} {target_clause}
            in the Creatio CRM schema.
            
            Your analysis should cover:
            1. Direct foreign key relationships
            2. Junction/bridge table relationships
            3. Detail relationships (parent-child patterns)
            4. Lookup references
            5. Cardinality of each relationship (1:1, 1:N, N:M)
            6. Common join patterns used in queries
            7. Relationship constraints and implications
            
            Consider how these relationships affect:
            - Query performance
            - Data integrity
            - Reporting capabilities
            - Data extraction patterns
            """,
            expected_output="""
            A detailed relationship analysis including:
            - Relationship Diagram (text representation)
            - Relationship Details (type, cardinality, columns)
            - Join Path Recommendations
            - Query Pattern Examples
            - Performance Considerations
            - Data Integrity Notes
            """,
            agent=agent,
        )
    
    @staticmethod
    def answer_schema_question(agent: Agent, question: str) -> Task:
        """
        Task to answer a specific question about the Creatio schema.
        
        Args:
            agent: The agent to assign this task to
            question: The user's question about the schema
        
        Returns:
            Task: The configured Q&A task
        """
        return Task(
            description=f"""
            Answer the following question about the Creatio CRM schema:
            
            QUESTION: {question}
            
            Provide a thorough, accurate answer by:
            1. Understanding the intent behind the question
            2. Using schema exploration tools to find relevant information
            3. Explaining the relevant parts of the schema
            4. Providing examples where helpful
            5. Noting any caveats or considerations
            
            If the question requires information not in the schema knowledge base,
            explain what additional data sources or documentation might be needed.
            """,
            expected_output="""
            A clear, comprehensive answer including:
            - Direct answer to the question
            - Supporting schema details
            - Relevant examples or queries
            - Additional context or considerations
            - References to related schema elements
            """,
            agent=agent,
        )
    
    @staticmethod
    def compare_entities(agent: Agent, entity1: str, entity2: str) -> Task:
        """
        Task to compare two entities in the schema.
        
        Args:
            agent: The agent to assign this task to
            entity1: First entity to compare
            entity2: Second entity to compare
        
        Returns:
            Task: The configured comparison task
        """
        return Task(
            description=f"""
            Compare the Creatio CRM entities {entity1} and {entity2}.
            
            Your comparison should include:
            1. Purpose and business function of each entity
            2. Structural similarities and differences
            3. Common columns across both entities
            4. Unique columns in each entity
            5. Relationship patterns for each
            6. When to use one vs the other
            7. How they might be used together
            
            This comparison should help users understand the role of each
            entity and how they fit into the overall CRM data model.
            """,
            expected_output="""
            An entity comparison report containing:
            - Side-by-side Overview
            - Structural Comparison (columns, types)
            - Relationship Comparison
            - Use Case Guidance
            - Integration Patterns (when used together)
            - Recommendations
            """,
            agent=agent,
        )
    
    @staticmethod
    def full_schema_overview(agent: Agent) -> Task:
        """
        Task to provide a complete schema overview.
        
        Args:
            agent: The agent to assign this task to
        
        Returns:
            Task: The configured overview task
        """
        return Task(
            description="""
            Provide a comprehensive overview of the Creatio CRM schema.
            
            Your overview should include:
            1. Core entities and their purposes (Contact, Account, Opportunity, etc.)
            2. Entity categories (master data, transactional, reference, system)
            3. Key relationship patterns used throughout the system
            4. Common design patterns in the schema
            5. The role of lookup tables
            6. How custom entities extend the base schema
            7. Tips for navigating and understanding the schema
            
            This overview should serve as an orientation for anyone new to
            the Creatio CRM data model.
            """,
            expected_output="""
            A complete schema overview document containing:
            - Executive Summary
            - Core Entity Catalog with descriptions
            - Entity Category Classification
            - Relationship Overview
            - Design Pattern Guide
            - Schema Navigation Tips
            - Glossary of Key Terms
            """,
            agent=agent,
        )
