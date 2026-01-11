"""
Creatio CRM Crew - Main crew orchestration module.

This module defines the main Crew class that orchestrates all agents
and their tasks for analyzing the Creatio CRM backend.
"""

from typing import Optional, List, Dict, Any
from crewai import Crew, Process

from creatio_crm_crew.agents import (
    SchemaAnalystAgent,
    DataArchitectAgent,
    MetricsExpertAgent,
    QueryBuilderAgent,
)
from creatio_crm_crew.tasks import (
    SchemaAnalysisTasks,
    QueryTasks,
    MetricsTasks,
    DocumentationTasks,
)
from creatio_crm_crew.tools import (
    # Schema tools
    SchemaExplorerTool,
    EntityRelationshipTool,
    ColumnAnalyzerTool,
    SchemaSearchTool,
    # Query tools
    SQLQueryBuilderTool,
    ODataQueryBuilderTool,
    QueryOptimizerTool,
    QueryValidatorTool,
    # Metrics tools
    MetricDefinitionTool,
    MetricCalculatorTool,
    KPILibraryTool,
    DashboardDesignerTool,
    # Documentation tools
    SchemaDocGeneratorTool,
    DataDictionaryTool,
    ERDGeneratorTool,
)
from creatio_crm_crew.config.settings import get_settings


class CreatioCRMCrew:
    """
    Main orchestration class for the Creatio CRM Backend Analysis system.
    
    This crew helps data architects and staff:
    - Understand the Creatio CRM database schema
    - Ask questions about data structure and relationships
    - Build efficient queries for data extraction
    - Define and calculate meaningful KPIs and metrics
    - Generate documentation and ERDs
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize the Creatio CRM Crew.
        
        Args:
            verbose: Whether to enable verbose output
        """
        self.settings = get_settings()
        self.verbose = verbose
        
        # Initialize tools
        self._init_tools()
        
        # Initialize agents
        self._init_agents()
    
    def _init_tools(self):
        """Initialize all tools."""
        # Schema exploration tools
        self.schema_tools = [
            SchemaExplorerTool(),
            EntityRelationshipTool(),
            ColumnAnalyzerTool(),
            SchemaSearchTool(),
        ]
        
        # Query building tools
        self.query_tools = [
            SQLQueryBuilderTool(),
            ODataQueryBuilderTool(),
            QueryOptimizerTool(),
            QueryValidatorTool(),
        ]
        
        # Metrics and KPI tools
        self.metrics_tools = [
            MetricDefinitionTool(),
            MetricCalculatorTool(),
            KPILibraryTool(),
            DashboardDesignerTool(),
        ]
        
        # Documentation tools
        self.documentation_tools = [
            SchemaDocGeneratorTool(),
            DataDictionaryTool(),
            ERDGeneratorTool(),
        ]
        
        # Combined tool sets for specific agents
        self.all_tools = (
            self.schema_tools + 
            self.query_tools + 
            self.metrics_tools + 
            self.documentation_tools
        )
    
    def _init_agents(self):
        """Initialize all agents with their respective tools."""
        # Schema Analyst - focuses on schema understanding
        self.schema_analyst = SchemaAnalystAgent.create(
            tools=self.schema_tools + self.documentation_tools
        )
        
        # Data Architect - provides architecture guidance
        self.data_architect = DataArchitectAgent.create(
            tools=self.schema_tools + self.query_tools + self.documentation_tools
        )
        
        # Metrics Expert - handles KPIs and analytics
        self.metrics_expert = MetricsExpertAgent.create(
            tools=self.metrics_tools + self.query_tools
        )
        
        # Query Builder - creates efficient queries
        self.query_builder = QueryBuilderAgent.create(
            tools=self.query_tools + self.schema_tools
        )
    
    # ==========================================================================
    # SCHEMA EXPLORATION METHODS
    # ==========================================================================
    
    def explore_entity(self, entity_name: str) -> str:
        """
        Explore a specific Creatio CRM entity.
        
        Args:
            entity_name: Name of the entity to explore
        
        Returns:
            Detailed entity analysis
        """
        task = SchemaAnalysisTasks.explore_entity(
            self.schema_analyst,
            entity_name
        )
        
        crew = Crew(
            agents=[self.schema_analyst],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def analyze_relationships(
        self, 
        source_entity: str, 
        target_entity: str = None
    ) -> str:
        """
        Analyze relationships between Creatio entities.
        
        Args:
            source_entity: Primary entity to analyze
            target_entity: Optional specific target entity
        
        Returns:
            Relationship analysis
        """
        task = SchemaAnalysisTasks.analyze_relationships(
            self.schema_analyst,
            source_entity,
            target_entity
        )
        
        crew = Crew(
            agents=[self.schema_analyst],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def ask_schema_question(self, question: str) -> str:
        """
        Answer a question about the Creatio CRM schema.
        
        Args:
            question: Question about the schema
        
        Returns:
            Answer to the question
        """
        task = SchemaAnalysisTasks.answer_schema_question(
            self.schema_analyst,
            question
        )
        
        crew = Crew(
            agents=[self.schema_analyst],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def get_schema_overview(self) -> str:
        """
        Get a complete overview of the Creatio CRM schema.
        
        Returns:
            Comprehensive schema overview
        """
        task = SchemaAnalysisTasks.full_schema_overview(
            self.schema_analyst
        )
        
        crew = Crew(
            agents=[self.schema_analyst],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    # ==========================================================================
    # QUERY BUILDING METHODS
    # ==========================================================================
    
    def build_query(self, question: str) -> str:
        """
        Build a query from a business question.
        
        Args:
            question: Business question to translate into a query
        
        Returns:
            SQL and OData queries with explanations
        """
        task = QueryTasks.build_query_from_question(
            self.query_builder,
            question
        )
        
        crew = Crew(
            agents=[self.query_builder],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def build_report_query(
        self, 
        report_description: str,
        entities: str,
        time_range: str = None
    ) -> str:
        """
        Build a SQL query for a report.
        
        Args:
            report_description: Description of the report
            entities: Main entities involved
            time_range: Optional time range
        
        Returns:
            Report query with documentation
        """
        task = QueryTasks.build_sql_report_query(
            self.query_builder,
            report_description,
            entities,
            time_range
        )
        
        crew = Crew(
            agents=[self.query_builder],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def optimize_query(self, query: str, query_type: str = "sql") -> str:
        """
        Optimize an existing query.
        
        Args:
            query: Query to optimize
            query_type: Type of query (sql or odata)
        
        Returns:
            Optimized query with analysis
        """
        task = QueryTasks.optimize_query(
            self.query_builder,
            query,
            query_type
        )
        
        crew = Crew(
            agents=[self.query_builder],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def build_odata_query(self, entity: str, requirements: str) -> str:
        """
        Build an OData query for the Creatio API.
        
        Args:
            entity: Primary entity to query
            requirements: Data requirements
        
        Returns:
            OData query with examples
        """
        task = QueryTasks.build_odata_query(
            self.query_builder,
            entity,
            requirements
        )
        
        crew = Crew(
            agents=[self.query_builder],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    # ==========================================================================
    # METRICS AND KPI METHODS
    # ==========================================================================
    
    def define_kpis(self, business_goal: str, context: str = "") -> str:
        """
        Define KPIs for a business goal.
        
        Args:
            business_goal: The business goal to measure
            context: Additional context
        
        Returns:
            KPI definitions with queries
        """
        task = MetricsTasks.define_kpi(
            self.metrics_expert,
            business_goal,
            context
        )
        
        crew = Crew(
            agents=[self.metrics_expert],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def calculate_metric(
        self, 
        metric_name: str, 
        time_period: str = "last_month",
        dimensions: str = None
    ) -> str:
        """
        Calculate a specific metric.
        
        Args:
            metric_name: Name of the metric
            time_period: Time period for calculation
            dimensions: Optional breakdown dimensions
        
        Returns:
            Metric calculation with query
        """
        task = MetricsTasks.calculate_metric(
            self.metrics_expert,
            metric_name,
            time_period,
            dimensions
        )
        
        crew = Crew(
            agents=[self.metrics_expert],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def recommend_metrics(self, role: str, focus_area: str) -> str:
        """
        Recommend metrics for a specific role.
        
        Args:
            role: User role (executive, manager, analyst, rep)
            focus_area: Business area of focus
        
        Returns:
            Metric recommendations
        """
        task = MetricsTasks.recommend_metrics_for_role(
            self.metrics_expert,
            role,
            focus_area
        )
        
        crew = Crew(
            agents=[self.metrics_expert],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def design_dashboard(self, purpose: str, audience: str) -> str:
        """
        Design a metrics dashboard.
        
        Args:
            purpose: Dashboard purpose
            audience: Target audience
        
        Returns:
            Dashboard design specification
        """
        task = MetricsTasks.design_dashboard(
            self.metrics_expert,
            purpose,
            audience
        )
        
        crew = Crew(
            agents=[self.metrics_expert],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def analyze_sales_pipeline(self, depth: str = "standard") -> str:
        """
        Analyze sales pipeline metrics.
        
        Args:
            depth: Analysis depth (quick, standard, deep)
        
        Returns:
            Pipeline analysis report
        """
        task = MetricsTasks.analyze_sales_pipeline(
            self.metrics_expert,
            depth
        )
        
        crew = Crew(
            agents=[self.metrics_expert],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def ask_metrics_question(self, question: str) -> str:
        """
        Answer a question about metrics and KPIs.
        
        Args:
            question: Question about metrics
        
        Returns:
            Answer with relevant metrics and queries
        """
        task = MetricsTasks.answer_metrics_question(
            self.metrics_expert,
            question
        )
        
        crew = Crew(
            agents=[self.metrics_expert],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    # ==========================================================================
    # DOCUMENTATION METHODS
    # ==========================================================================
    
    def generate_documentation(self, entities: str = "all") -> str:
        """
        Generate documentation for Creatio entities.
        
        Args:
            entities: Comma-separated entity list or 'all'
        
        Returns:
            Comprehensive documentation
        """
        task = DocumentationTasks.generate_entity_documentation(
            self.data_architect,
            entities
        )
        
        crew = Crew(
            agents=[self.data_architect],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def create_data_dictionary(self, entity: str) -> str:
        """
        Create a data dictionary for an entity.
        
        Args:
            entity: Entity to document
        
        Returns:
            Data dictionary
        """
        task = DocumentationTasks.create_data_dictionary(
            self.data_architect,
            entity
        )
        
        crew = Crew(
            agents=[self.data_architect],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def generate_erd(self, entities: str, include_columns: bool = True) -> str:
        """
        Generate an Entity-Relationship Diagram.
        
        Args:
            entities: Entities to include
            include_columns: Whether to include column details
        
        Returns:
            ERD in multiple formats
        """
        task = DocumentationTasks.generate_erd(
            self.data_architect,
            entities,
            include_columns
        )
        
        crew = Crew(
            agents=[self.data_architect],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def create_integration_guide(
        self, 
        source_system: str, 
        target_entities: str
    ) -> str:
        """
        Create an integration guide.
        
        Args:
            source_system: External system
            target_entities: Creatio entities to integrate
        
        Returns:
            Integration guide
        """
        task = DocumentationTasks.create_integration_guide(
            self.data_architect,
            source_system,
            target_entities
        )
        
        crew = Crew(
            agents=[self.data_architect],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    # ==========================================================================
    # COMPOSITE WORKFLOWS
    # ==========================================================================
    
    def comprehensive_entity_analysis(self, entity: str) -> str:
        """
        Perform comprehensive analysis of an entity.
        
        Combines schema analysis, query patterns, and documentation.
        
        Args:
            entity: Entity to analyze
        
        Returns:
            Comprehensive entity analysis
        """
        tasks = [
            # Schema exploration
            SchemaAnalysisTasks.explore_entity(
                self.schema_analyst,
                entity
            ),
            # Query patterns
            QueryTasks.create_reusable_query_template(
                self.query_builder,
                f"Standard CRUD operations for {entity}",
                "id, filters, pagination"
            ),
            # Data dictionary
            DocumentationTasks.create_data_dictionary(
                self.data_architect,
                entity
            ),
        ]
        
        crew = Crew(
            agents=[self.schema_analyst, self.query_builder, self.data_architect],
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def full_metrics_analysis(
        self, 
        business_area: str,
        audience: str = "manager"
    ) -> str:
        """
        Perform full metrics analysis for a business area.
        
        Args:
            business_area: Business area to analyze
            audience: Target audience
        
        Returns:
            Complete metrics analysis with dashboard design
        """
        tasks = [
            # KPI definition
            MetricsTasks.define_kpi(
                self.metrics_expert,
                f"Measure performance in {business_area}",
                f"For {audience} audience"
            ),
            # Dashboard design
            MetricsTasks.design_dashboard(
                self.metrics_expert,
                f"{business_area} Performance Dashboard",
                audience
            ),
        ]
        
        crew = Crew(
            agents=[self.metrics_expert],
            tasks=tasks,
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def ask_question(self, question: str) -> str:
        """
        Answer any question about Creatio CRM backend.
        
        This is the main entry point for ad-hoc questions.
        Routes to the most appropriate agent based on question content.
        
        Args:
            question: Any question about Creatio CRM
        
        Returns:
            Comprehensive answer
        """
        question_lower = question.lower()
        
        # Determine the best agent and task based on question content
        if any(word in question_lower for word in ['schema', 'table', 'column', 'entity', 'relationship', 'structure']):
            task = SchemaAnalysisTasks.answer_schema_question(
                self.schema_analyst,
                question
            )
            agent = self.schema_analyst
        elif any(word in question_lower for word in ['query', 'sql', 'odata', 'select', 'join', 'extract']):
            task = QueryTasks.build_query_from_question(
                self.query_builder,
                question
            )
            agent = self.query_builder
        elif any(word in question_lower for word in ['kpi', 'metric', 'measure', 'dashboard', 'report', 'analytics']):
            task = MetricsTasks.answer_metrics_question(
                self.metrics_expert,
                question
            )
            agent = self.metrics_expert
        else:
            # Default to schema analyst for general questions
            task = SchemaAnalysisTasks.answer_schema_question(
                self.schema_analyst,
                question
            )
            agent = self.schema_analyst
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose,
        )
        
        return crew.kickoff()
    
    def run_custom_workflow(self, workflow_config: Dict[str, Any]) -> str:
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
            "schema_analyst": self.schema_analyst,
            "data_architect": self.data_architect,
            "metrics_expert": self.metrics_expert,
            "query_builder": self.query_builder,
        }
        
        agents = [
            agent_map[name] 
            for name in workflow_config.get("agents", ["schema_analyst"])
            if name in agent_map
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
            agent_name = task_config.get("agent", "schema_analyst")
            agent = agent_map.get(agent_name, self.schema_analyst)
            
            # Map task types to task functions
            if task_type == "explore_entity":
                task = SchemaAnalysisTasks.explore_entity(
                    agent,
                    task_config.get("entity", "Contact")
                )
            elif task_type == "build_query":
                task = QueryTasks.build_query_from_question(
                    agent,
                    task_config.get("question", "")
                )
            elif task_type == "define_kpi":
                task = MetricsTasks.define_kpi(
                    agent,
                    task_config.get("goal", ""),
                    task_config.get("context", "")
                )
            elif task_type == "generate_documentation":
                task = DocumentationTasks.generate_entity_documentation(
                    agent,
                    task_config.get("entities", "Contact")
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
