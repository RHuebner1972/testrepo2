"""
Tasks for metrics and KPI analysis in Creatio CRM.
"""

from crewai import Task, Agent


class MetricsTasks:
    """Task definitions for metrics and KPI analysis."""
    
    @staticmethod
    def define_kpi(agent: Agent, business_goal: str, context: str) -> Task:
        """
        Task to define KPIs for a business goal.
        
        Args:
            agent: The agent to assign this task to
            business_goal: The business goal to measure
            context: Additional context about the use case
        
        Returns:
            Task: The configured KPI definition task
        """
        return Task(
            description=f"""
            Define Key Performance Indicators (KPIs) for the following business goal:
            
            BUSINESS GOAL: {business_goal}
            CONTEXT: {context}
            
            Your KPI definition should include:
            1. Primary KPIs that directly measure the goal
            2. Supporting KPIs that provide context
            3. Leading indicators (predictive metrics)
            4. Lagging indicators (outcome metrics)
            5. For each KPI:
               - Clear definition and formula
               - Data sources in Creatio
               - Calculation method
               - Recommended targets/benchmarks
               - Measurement frequency
               - Visualization recommendations
            
            Ensure all KPIs can be calculated from available Creatio CRM data.
            """,
            expected_output="""
            A comprehensive KPI definition document containing:
            - Executive Summary
            - Primary KPIs (3-5 key metrics)
            - Supporting KPIs
            - For each KPI:
              - Name and Definition
              - Formula/Calculation
              - Data Source (entities, columns)
              - SQL Query
              - Target/Benchmark
              - Frequency
              - Visualization Type
            - Implementation Roadmap
            - Dashboard Recommendations
            """,
            agent=agent,
        )
    
    @staticmethod
    def calculate_metric(
        agent: Agent, 
        metric_name: str, 
        time_period: str,
        dimensions: str = None
    ) -> Task:
        """
        Task to calculate a specific metric.
        
        Args:
            agent: The agent to assign this task to
            metric_name: Name of the metric to calculate
            time_period: Time period for calculation
            dimensions: Optional dimensions for breakdown
        
        Returns:
            Task: The configured calculation task
        """
        dimension_clause = f"DIMENSIONS: {dimensions}" if dimensions else ""
        
        return Task(
            description=f"""
            Calculate the following metric from Creatio CRM data:
            
            METRIC: {metric_name}
            TIME PERIOD: {time_period}
            {dimension_clause}
            
            Your calculation should include:
            1. Identify the exact metric definition
            2. Determine required data sources
            3. Build the calculation query
            4. Include appropriate time filters
            5. Add dimensional breakdowns if specified
            6. Provide calculation methodology
            7. Note any data quality considerations
            
            Provide the SQL query that would calculate this metric
            along with explanation of the calculation logic.
            """,
            expected_output="""
            A metric calculation package containing:
            - Metric Definition
            - SQL Calculation Query
            - Calculation Methodology
            - Sample Output Format
            - Data Quality Notes
            - Interpretation Guidance
            - Related Metrics to Consider
            """,
            agent=agent,
        )
    
    @staticmethod
    def recommend_metrics_for_role(agent: Agent, role: str, focus_area: str) -> Task:
        """
        Task to recommend metrics for a specific role.
        
        Args:
            agent: The agent to assign this task to
            role: User role (executive, manager, analyst, rep)
            focus_area: Business area of focus
        
        Returns:
            Task: The configured recommendation task
        """
        return Task(
            description=f"""
            Recommend key metrics for a {role} focused on {focus_area}.
            
            Consider:
            1. What decisions does this role need to make?
            2. What information helps those decisions?
            3. What level of detail is appropriate?
            4. What time horizons matter?
            5. What benchmarks are relevant?
            
            For each recommended metric:
            - Explain why it matters for this role
            - How often it should be reviewed
            - What actions it should trigger
            - How to present it effectively
            
            Use the KPI library to identify relevant metrics and suggest
            customizations for this specific use case.
            """,
            expected_output="""
            A role-specific metrics recommendation containing:
            - Role Overview and Key Decisions
            - Top 5-10 Recommended Metrics
            - For each metric:
              - Name and Definition
              - Why It Matters for This Role
              - Review Frequency
              - Action Triggers
              - Presentation Format
            - Dashboard Layout Suggestion
            - Alert/Notification Recommendations
            """,
            agent=agent,
        )
    
    @staticmethod
    def design_dashboard(agent: Agent, dashboard_purpose: str, audience: str) -> Task:
        """
        Task to design a metrics dashboard.
        
        Args:
            agent: The agent to assign this task to
            dashboard_purpose: Purpose of the dashboard
            audience: Target audience
        
        Returns:
            Task: The configured dashboard design task
        """
        return Task(
            description=f"""
            Design a metrics dashboard for Creatio CRM data:
            
            PURPOSE: {dashboard_purpose}
            AUDIENCE: {audience}
            
            Your dashboard design should include:
            1. Dashboard objectives and key questions answered
            2. Selected KPIs and metrics
            3. Widget layout and types
            4. Time range controls
            5. Filter/drill-down capabilities
            6. Data refresh frequency
            7. Color coding and alert thresholds
            8. Mobile/responsive considerations
            
            For each widget:
            - Metric displayed
            - Visualization type
            - Data source query
            - Size and position
            - Interaction capabilities
            """,
            expected_output="""
            A comprehensive dashboard design document containing:
            - Dashboard Overview
            - Key Questions Answered
            - Widget Specifications:
              - Layout diagram (text-based)
              - Widget details (metric, type, size)
              - Query for each widget
            - Interactivity Design
            - Filtering Options
            - Alert Configuration
            - Implementation Guide for Creatio
            """,
            agent=agent,
        )
    
    @staticmethod
    def analyze_sales_pipeline(agent: Agent, analysis_depth: str = "standard") -> Task:
        """
        Task to analyze sales pipeline metrics.
        
        Args:
            agent: The agent to assign this task to
            analysis_depth: Level of analysis (quick, standard, deep)
        
        Returns:
            Task: The configured pipeline analysis task
        """
        return Task(
            description=f"""
            Perform a {analysis_depth} analysis of sales pipeline metrics in Creatio CRM.
            
            Your analysis should include:
            1. Pipeline Value (total, by stage, by owner)
            2. Pipeline Velocity
            3. Stage Conversion Rates
            4. Average Deal Size
            5. Sales Cycle Length
            6. Win/Loss Analysis
            7. Pipeline Coverage Ratio
            8. Forecast Accuracy (if historical data available)
            
            For each metric:
            - Current value
            - Trend analysis
            - Comparison to targets/benchmarks
            - Key insights and anomalies
            - Recommended actions
            
            Provide the queries needed to extract this data from Creatio.
            """,
            expected_output="""
            A sales pipeline analysis report containing:
            - Executive Summary
            - Key Metrics Dashboard
            - Pipeline Health Assessment
            - Stage-by-Stage Analysis
            - Owner/Team Performance
            - Trend Analysis
            - Risk Areas
            - Recommendations
            - Data Extraction Queries
            """,
            agent=agent,
        )
    
    @staticmethod
    def build_metric_comparison(
        agent: Agent, 
        metric: str, 
        comparison_type: str,
        segments: str
    ) -> Task:
        """
        Task to build metric comparisons.
        
        Args:
            agent: The agent to assign this task to
            metric: Metric to compare
            comparison_type: Type of comparison (period, segment, benchmark)
            segments: Segments or periods to compare
        
        Returns:
            Task: The configured comparison task
        """
        return Task(
            description=f"""
            Build a comparison analysis for the following metric:
            
            METRIC: {metric}
            COMPARISON TYPE: {comparison_type}
            SEGMENTS/PERIODS: {segments}
            
            Your comparison should include:
            1. Metric definition and calculation
            2. Values for each segment/period
            3. Variance analysis (absolute and percentage)
            4. Statistical significance (if applicable)
            5. Visual representation recommendation
            6. Key findings and insights
            7. Potential explanations for differences
            
            Provide the SQL queries needed to extract the comparison data.
            """,
            expected_output="""
            A metric comparison report containing:
            - Comparison Summary Table
            - SQL Queries for Data Extraction
            - Variance Analysis
            - Visualization Recommendation
            - Key Insights
            - Statistical Notes
            - Action Recommendations
            """,
            agent=agent,
        )
    
    @staticmethod
    def answer_metrics_question(agent: Agent, question: str) -> Task:
        """
        Task to answer a question about metrics.
        
        Args:
            agent: The agent to assign this task to
            question: The user's metrics question
        
        Returns:
            Task: The configured Q&A task
        """
        return Task(
            description=f"""
            Answer the following question about metrics and KPIs in Creatio CRM:
            
            QUESTION: {question}
            
            Provide a thorough answer that:
            1. Directly addresses the question
            2. References relevant standard KPIs
            3. Provides calculation formulas if applicable
            4. Includes data sources and queries
            5. Offers best practices and recommendations
            6. Notes any caveats or considerations
            
            If the question involves custom metrics, help define them
            based on Creatio's data model.
            """,
            expected_output="""
            A comprehensive answer containing:
            - Direct Answer
            - Relevant KPIs/Metrics
            - Formulas and Calculations
            - SQL/OData Queries
            - Best Practices
            - Additional Considerations
            - Related Metrics to Explore
            """,
            agent=agent,
        )
