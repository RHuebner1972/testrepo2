"""
Tasks for documentation generation in Creatio CRM.
"""

from crewai import Task, Agent


class DocumentationTasks:
    """Task definitions for documentation generation."""
    
    @staticmethod
    def generate_entity_documentation(agent: Agent, entities: str) -> Task:
        """
        Task to generate comprehensive entity documentation.
        
        Args:
            agent: The agent to assign this task to
            entities: Comma-separated list of entities or 'all'
        
        Returns:
            Task: The configured documentation task
        """
        return Task(
            description=f"""
            Generate comprehensive documentation for Creatio CRM entities: {entities}
            
            The documentation should include for each entity:
            1. Entity overview and business purpose
            2. Database table mapping
            3. Complete column reference
               - Column name
               - Data type
               - Description
               - Constraints
               - Business rules
            4. Relationships with other entities
            5. Common query patterns
            6. Best practices for working with the entity
            7. Example queries (SELECT, with JOINs)
            
            Format the documentation for easy reference by:
            - Data architects
            - Database developers
            - Report builders
            - Integration specialists
            """,
            expected_output="""
            Complete entity documentation containing:
            - Table of Contents
            - Entity Overview Sections
            - Column Reference Tables
            - Relationship Diagrams (text format)
            - Query Examples
            - Best Practices Guide
            - Glossary of Terms
            """,
            agent=agent,
        )
    
    @staticmethod
    def create_data_dictionary(agent: Agent, entity: str) -> Task:
        """
        Task to create a data dictionary for an entity.
        
        Args:
            agent: The agent to assign this task to
            entity: Entity to document
        
        Returns:
            Task: The configured data dictionary task
        """
        return Task(
            description=f"""
            Create a detailed data dictionary for the Creatio CRM entity: {entity}
            
            The data dictionary should include:
            1. Entity metadata (name, table, description)
            2. For each column:
               - Physical name
               - Logical/business name
               - Data type with precision
               - Nullable flag
               - Primary/foreign key indicator
               - Referenced table for FKs
               - Default value
               - Business definition
               - Valid values or ranges
               - Data quality rules
               - Sample values
            3. Indexes (recommended)
            4. Audit column documentation
            5. Related lookup tables
            
            This should serve as a complete reference for anyone
            working with this entity's data.
            """,
            expected_output="""
            A complete data dictionary containing:
            - Entity Header (name, table, description)
            - Column Catalog Table
            - Primary Key Documentation
            - Foreign Key References
            - Index Recommendations
            - Business Rules
            - Lookup Value References
            - Data Quality Guidelines
            - Audit Information
            """,
            agent=agent,
        )
    
    @staticmethod
    def generate_erd(agent: Agent, entities: str, include_details: bool = True) -> Task:
        """
        Task to generate an Entity-Relationship Diagram.
        
        Args:
            agent: The agent to assign this task to
            entities: Entities to include in the ERD
            include_details: Whether to include column details
        
        Returns:
            Task: The configured ERD generation task
        """
        detail_clause = "with column details" if include_details else "entity names only"
        
        return Task(
            description=f"""
            Generate an Entity-Relationship Diagram for Creatio CRM entities: {entities}
            Format: {detail_clause}
            
            The ERD should:
            1. Show all specified entities
            2. Display relationships between entities
            3. Indicate relationship cardinality (1:1, 1:N, N:M)
            4. Include column details if requested
            5. Mark primary and foreign keys
            6. Use standard ERD notation
            
            Generate the diagram in multiple formats:
            - Mermaid (for GitHub/GitLab rendering)
            - PlantUML (for documentation tools)
            - DBML (for dbdiagram.io)
            
            Include rendering instructions for each format.
            """,
            expected_output="""
            An ERD package containing:
            - Mermaid Diagram Code
            - PlantUML Diagram Code
            - DBML Code
            - Rendering Instructions
            - Relationship Legend
            - Usage Notes
            """,
            agent=agent,
        )
    
    @staticmethod
    def document_query_pattern(agent: Agent, pattern_name: str, use_case: str) -> Task:
        """
        Task to document a query pattern.
        
        Args:
            agent: The agent to assign this task to
            pattern_name: Name of the pattern
            use_case: Use case for the pattern
        
        Returns:
            Task: The configured documentation task
        """
        return Task(
            description=f"""
            Document the following query pattern for Creatio CRM:
            
            PATTERN: {pattern_name}
            USE CASE: {use_case}
            
            Your documentation should include:
            1. Pattern name and description
            2. When to use this pattern
            3. Prerequisites and requirements
            4. Step-by-step query building
            5. Complete example query
            6. Performance considerations
            7. Common variations
            8. Anti-patterns to avoid
            9. Related patterns
            
            This documentation should enable developers to implement
            the pattern correctly in their own queries.
            """,
            expected_output="""
            Query pattern documentation containing:
            - Pattern Overview
            - Use Cases
            - Prerequisites
            - Implementation Guide
            - Example Queries
            - Performance Notes
            - Variations
            - Anti-patterns
            - Best Practices
            """,
            agent=agent,
        )
    
    @staticmethod
    def create_integration_guide(
        agent: Agent, 
        source_system: str, 
        target_entities: str
    ) -> Task:
        """
        Task to create an integration guide.
        
        Args:
            agent: The agent to assign this task to
            source_system: External system integrating with Creatio
            target_entities: Creatio entities involved
        
        Returns:
            Task: The configured integration guide task
        """
        return Task(
            description=f"""
            Create an integration guide for connecting {source_system} with Creatio CRM.
            Target entities: {target_entities}
            
            The guide should include:
            1. Integration overview and scope
            2. Creatio entity details for target entities
            3. Field mapping recommendations
            4. Data type considerations
            5. OData API endpoints for each entity
            6. Authentication requirements
            7. Sample API requests (CRUD operations)
            8. Error handling guidance
            9. Best practices for data synchronization
            10. Common pitfalls and solutions
            
            This should enable a developer to implement the integration
            without deep Creatio knowledge.
            """,
            expected_output="""
            An integration guide containing:
            - Integration Overview
            - Entity Schema Reference
            - Field Mapping Table
            - API Endpoint Catalog
            - Authentication Guide
            - Sample API Requests (curl/code)
            - Error Handling
            - Sync Strategy Recommendations
            - Troubleshooting Guide
            """,
            agent=agent,
        )
    
    @staticmethod
    def generate_report_specification(
        agent: Agent, 
        report_name: str, 
        requirements: str
    ) -> Task:
        """
        Task to generate a report specification.
        
        Args:
            agent: The agent to assign this task to
            report_name: Name of the report
            requirements: Report requirements
        
        Returns:
            Task: The configured specification task
        """
        return Task(
            description=f"""
            Generate a technical specification for the following report:
            
            REPORT NAME: {report_name}
            REQUIREMENTS: {requirements}
            
            The specification should include:
            1. Report overview and purpose
            2. Target audience
            3. Data sources (entities, columns)
            4. Filters and parameters
            5. Column specifications:
               - Display name
               - Source field
               - Data type
               - Format
               - Aggregation (if any)
            6. Grouping and sorting
            7. Calculations and derived fields
            8. SQL query for data extraction
            9. Layout recommendations
            10. Distribution and access
            
            This specification should be detailed enough for a developer
            to build the report without additional clarification.
            """,
            expected_output="""
            A report specification containing:
            - Report Header (name, purpose, audience)
            - Data Source Documentation
            - Column Specifications Table
            - Filter/Parameter Definitions
            - Calculation Formulas
            - SQL Query
            - Layout Mockup (text)
            - Implementation Notes
            - Testing Checklist
            """,
            agent=agent,
        )
    
    @staticmethod
    def answer_documentation_question(agent: Agent, question: str) -> Task:
        """
        Task to answer a documentation-related question.
        
        Args:
            agent: The agent to assign this task to
            question: The user's documentation question
        
        Returns:
            Task: The configured Q&A task
        """
        return Task(
            description=f"""
            Answer the following documentation question about Creatio CRM:
            
            QUESTION: {question}
            
            Provide a thorough answer that:
            1. Directly addresses the question
            2. Includes relevant schema information
            3. Provides examples where helpful
            4. References proper documentation formats
            5. Suggests additional resources if available
            
            If the question requires generating documentation,
            create the appropriate documentation artifacts.
            """,
            expected_output="""
            A comprehensive answer containing:
            - Direct Answer
            - Supporting Documentation
            - Examples/Samples
            - References
            - Additional Resources
            """,
            agent=agent,
        )
