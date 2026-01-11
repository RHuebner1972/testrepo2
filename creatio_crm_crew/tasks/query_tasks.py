"""
Tasks for query building and optimization in Creatio CRM.
"""

from crewai import Task, Agent


class QueryTasks:
    """Task definitions for query building."""
    
    @staticmethod
    def build_query_from_question(agent: Agent, question: str) -> Task:
        """
        Task to build a query from a business question.
        
        Args:
            agent: The agent to assign this task to
            question: Business question to translate into a query
        
        Returns:
            Task: The configured query building task
        """
        return Task(
            description=f"""
            Translate the following business question into an efficient query
            for Creatio CRM data:
            
            QUESTION: {question}
            
            Your process should include:
            1. Analyze the question to understand data requirements
            2. Identify the relevant Creatio entities and columns
            3. Determine necessary joins and relationships
            4. Define appropriate filters and conditions
            5. Consider aggregations if needed
            6. Build both SQL and OData versions of the query
            7. Validate the query for correctness
            8. Optimize for performance
            
            The query should be ready to execute against Creatio's database
            or API, with clear explanations of what each part does.
            """,
            expected_output="""
            A complete query solution containing:
            - Interpreted Requirements (what data is needed)
            - Entities and Columns Used
            - SQL Query (with comments)
            - OData Query (API version)
            - Explanation of Query Logic
            - Performance Notes
            - Potential Variations
            """,
            agent=agent,
        )
    
    @staticmethod
    def build_sql_report_query(
        agent: Agent, 
        report_description: str,
        entities: str,
        time_range: str = None
    ) -> Task:
        """
        Task to build a SQL query for reporting.
        
        Args:
            agent: The agent to assign this task to
            report_description: Description of the report needed
            entities: Main entities involved
            time_range: Optional time range filter
        
        Returns:
            Task: The configured report query task
        """
        time_clause = f"Time Range: {time_range}" if time_range else ""
        
        return Task(
            description=f"""
            Build a SQL query for the following report requirement:
            
            REPORT: {report_description}
            ENTITIES: {entities}
            {time_clause}
            
            Your query should:
            1. Extract all necessary columns for the report
            2. Include proper joins between entities
            3. Apply appropriate filters and date ranges
            4. Include aggregations and groupings as needed
            5. Use efficient query patterns
            6. Include comments explaining each section
            7. Be formatted for readability
            
            Also provide:
            - Sample output structure
            - Estimated data volume considerations
            - Index recommendations for performance
            """,
            expected_output="""
            A complete report query package containing:
            - SQL Query (fully commented)
            - Output Column Descriptions
            - Query Execution Notes
            - Performance Optimization Tips
            - Index Recommendations
            - Sample Data Preview Structure
            """,
            agent=agent,
        )
    
    @staticmethod
    def build_odata_query(
        agent: Agent,
        entity: str,
        requirements: str
    ) -> Task:
        """
        Task to build an OData query for Creatio API.
        
        Args:
            agent: The agent to assign this task to
            entity: Primary entity to query
            requirements: Data requirements
        
        Returns:
            Task: The configured OData query task
        """
        return Task(
            description=f"""
            Build an OData query for accessing {entity} data via Creatio API.
            
            REQUIREMENTS: {requirements}
            
            Your OData query should include:
            1. Proper entity collection URL
            2. $select for specific columns
            3. $filter for conditions
            4. $expand for related entities (if needed)
            5. $orderby for sorting
            6. $top and $skip for pagination
            7. Any necessary query options
            
            Also provide:
            - Complete URL example
            - CURL command for testing
            - Response structure preview
            - Pagination implementation guidance
            - Error handling considerations
            """,
            expected_output="""
            A complete OData query solution containing:
            - OData URL with all parameters
            - CURL example command
            - JavaScript/Python fetch example
            - Expected response structure
            - Pagination strategy
            - Error handling notes
            """,
            agent=agent,
        )
    
    @staticmethod
    def optimize_query(agent: Agent, query: str, query_type: str = "sql") -> Task:
        """
        Task to optimize an existing query.
        
        Args:
            agent: The agent to assign this task to
            query: Query to optimize
            query_type: Type of query (sql or odata)
        
        Returns:
            Task: The configured optimization task
        """
        return Task(
            description=f"""
            Optimize the following {query_type.upper()} query for better performance:
            
            QUERY:
            {query}
            
            Your optimization should address:
            1. Query structure efficiency
            2. Join optimization
            3. Filter placement and selectivity
            4. Column selection (avoid SELECT *)
            5. Index utilization
            6. Subquery vs JOIN decisions
            7. Aggregation efficiency
            8. Pagination optimization
            
            Provide both the optimized query and a detailed explanation
            of the changes made and their expected impact.
            """,
            expected_output="""
            A query optimization report containing:
            - Original Query Analysis
            - Identified Issues
            - Optimized Query
            - Changes Made (with explanations)
            - Expected Performance Improvement
            - Index Recommendations
            - Before/After Comparison
            """,
            agent=agent,
        )
    
    @staticmethod
    def create_reusable_query_template(
        agent: Agent,
        use_case: str,
        parameters: str
    ) -> Task:
        """
        Task to create a reusable query template.
        
        Args:
            agent: The agent to assign this task to
            use_case: Description of the use case
            parameters: Parameters that should be configurable
        
        Returns:
            Task: The configured template creation task
        """
        return Task(
            description=f"""
            Create a reusable query template for the following use case:
            
            USE CASE: {use_case}
            PARAMETERS: {parameters}
            
            Your template should include:
            1. Parameterized SQL query with placeholders
            2. OData equivalent with parameter substitution
            3. Clear parameter documentation
            4. Default values where appropriate
            5. Validation rules for parameters
            6. Usage examples with different parameter values
            7. Error handling for invalid parameters
            
            The template should be production-ready and easy to integrate
            into applications or reporting tools.
            """,
            expected_output="""
            A reusable query template package containing:
            - SQL Template (with parameters)
            - OData Template
            - Parameter Documentation
            - Default Values
            - Usage Examples
            - Integration Guide
            - Testing Suggestions
            """,
            agent=agent,
        )
    
    @staticmethod
    def validate_and_fix_query(agent: Agent, query: str) -> Task:
        """
        Task to validate and fix a query.
        
        Args:
            agent: The agent to assign this task to
            query: Query to validate
        
        Returns:
            Task: The configured validation task
        """
        return Task(
            description=f"""
            Validate the following query for correctness and fix any issues:
            
            QUERY:
            {query}
            
            Your validation should check:
            1. Syntax correctness
            2. Entity/table references
            3. Column name accuracy
            4. Join conditions
            5. Filter logic
            6. Aggregation correctness
            7. Common anti-patterns
            8. Security considerations (SQL injection risks)
            
            If issues are found, provide corrected versions with explanations.
            """,
            expected_output="""
            A query validation report containing:
            - Validation Results (pass/fail for each check)
            - Issues Found (if any)
            - Corrected Query
            - Explanation of Fixes
            - Security Assessment
            - Best Practice Recommendations
            """,
            agent=agent,
        )
