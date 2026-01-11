"""
Tests for the Creatio CRM Backend Analysis Crew.
"""

import pytest
from unittest.mock import patch, MagicMock


class TestSchemaTools:
    """Tests for schema exploration tools."""
    
    def test_schema_explorer_tool_known_entity(self):
        """Test schema explorer with known entity."""
        from creatio_crm_crew.tools.schema_tools import SchemaExplorerTool
        
        tool = SchemaExplorerTool()
        result = tool._run("Contact", include_relationships=True)
        
        assert "success" in result
        assert "Contact" in result
        assert "table_name" in result
    
    def test_schema_explorer_tool_unknown_entity(self):
        """Test schema explorer with unknown entity."""
        from creatio_crm_crew.tools.schema_tools import SchemaExplorerTool
        
        tool = SchemaExplorerTool()
        result = tool._run("UnknownEntity")
        
        assert "success" in result
        assert "False" in result or "error" in result.lower()
    
    def test_entity_relationship_tool(self):
        """Test entity relationship analysis."""
        from creatio_crm_crew.tools.schema_tools import EntityRelationshipTool
        
        tool = EntityRelationshipTool()
        result = tool._run("Contact", "Account", relationship_depth=2)
        
        assert "success" in result
        assert "direct_relationships" in result
    
    def test_column_analyzer_tool(self):
        """Test column analyzer."""
        from creatio_crm_crew.tools.schema_tools import ColumnAnalyzerTool
        
        tool = ColumnAnalyzerTool()
        result = tool._run("Contact", column_filter="Email")
        
        assert "success" in result
        assert "columns" in result
    
    def test_schema_search_tool(self):
        """Test schema search."""
        from creatio_crm_crew.tools.schema_tools import SchemaSearchTool
        
        tool = SchemaSearchTool()
        result = tool._run("email", search_scope="all")
        
        assert "success" in result
        assert "matches" in result


class TestQueryTools:
    """Tests for query building tools."""
    
    def test_sql_query_builder(self):
        """Test SQL query builder."""
        from creatio_crm_crew.tools.query_tools import SQLQueryBuilderTool
        
        tool = SQLQueryBuilderTool()
        result = tool._run(
            objective="Get all contacts with accounts",
            entities="Contact, Account",
            filters="active contacts"
        )
        
        assert "success" in result
        assert "query" in result
        assert "SELECT" in result
    
    def test_odata_query_builder(self):
        """Test OData query builder."""
        from creatio_crm_crew.tools.query_tools import ODataQueryBuilderTool
        
        tool = ODataQueryBuilderTool()
        result = tool._run(
            entity="Contact",
            select_fields="Name,Email",
            filter_expression="active",
            top=50
        )
        
        assert "success" in result
        assert "odata_url" in result
        assert "$select" in result
    
    def test_query_optimizer(self):
        """Test query optimizer."""
        from creatio_crm_crew.tools.query_tools import QueryOptimizerTool
        
        tool = QueryOptimizerTool()
        result = tool._run(
            query="SELECT * FROM Contact",
            query_type="sql",
            optimization_goal="performance"
        )
        
        assert "success" in result
        assert "recommendations" in result
    
    def test_query_validator(self):
        """Test query validator."""
        from creatio_crm_crew.tools.query_tools import QueryValidatorTool
        
        tool = QueryValidatorTool()
        result = tool._run(
            query="SELECT Id, Name FROM Contact WHERE AccountId IS NOT NULL",
            query_type="sql"
        )
        
        assert "success" in result
        assert "is_valid" in result


class TestMetricsTools:
    """Tests for metrics and KPI tools."""
    
    def test_metric_definition_tool(self):
        """Test metric definition."""
        from creatio_crm_crew.tools.metrics_tools import MetricDefinitionTool
        
        tool = MetricDefinitionTool()
        result = tool._run(
            metric_name="lead conversion rate",
            business_context="sales team performance",
            target_entity="Lead"
        )
        
        assert "success" in result
        assert "custom_definition" in result
    
    def test_metric_calculator_tool(self):
        """Test metric calculator."""
        from creatio_crm_crew.tools.metrics_tools import MetricCalculatorTool
        
        tool = MetricCalculatorTool()
        result = tool._run(
            metric_id="sales.win_rate",
            time_period="last_month"
        )
        
        assert "success" in result
        assert "calculation" in result
    
    def test_metric_calculator_invalid_metric(self):
        """Test metric calculator with invalid metric."""
        from creatio_crm_crew.tools.metrics_tools import MetricCalculatorTool
        
        tool = MetricCalculatorTool()
        result = tool._run(
            metric_id="invalid.metric",
            time_period="last_month"
        )
        
        assert "success" in result
        assert "False" in result or "error" in result.lower()
    
    def test_kpi_library_tool(self):
        """Test KPI library browsing."""
        from creatio_crm_crew.tools.metrics_tools import KPILibraryTool
        
        tool = KPILibraryTool()
        result = tool._run(category="sales")
        
        assert "success" in result
        assert "kpis" in result
    
    def test_dashboard_designer_tool(self):
        """Test dashboard designer."""
        from creatio_crm_crew.tools.metrics_tools import DashboardDesignerTool
        
        tool = DashboardDesignerTool()
        result = tool._run(
            dashboard_purpose="Sales performance overview",
            audience="manager",
            key_questions="How is the pipeline? What is our win rate?"
        )
        
        assert "success" in result
        assert "design" in result
        assert "recommended_kpis" in result


class TestDocumentationTools:
    """Tests for documentation generation tools."""
    
    def test_schema_doc_generator(self):
        """Test schema documentation generator."""
        from creatio_crm_crew.tools.documentation_tools import SchemaDocGeneratorTool
        
        tool = SchemaDocGeneratorTool()
        result = tool._run(
            entities="Contact, Account",
            format="markdown",
            include_relationships=True
        )
        
        assert "success" in result
        assert "documentation" in result
    
    def test_data_dictionary_tool(self):
        """Test data dictionary generation."""
        from creatio_crm_crew.tools.documentation_tools import DataDictionaryTool
        
        tool = DataDictionaryTool()
        result = tool._run(entity="Opportunity")
        
        assert "success" in result
        assert "data_dictionary" in result
    
    def test_erd_generator_tool(self):
        """Test ERD generation."""
        from creatio_crm_crew.tools.documentation_tools import ERDGeneratorTool
        
        tool = ERDGeneratorTool()
        result = tool._run(
            entities="Contact, Account",
            format="mermaid",
            show_columns=True
        )
        
        assert "success" in result
        assert "diagram" in result
        assert "erDiagram" in result


class TestAgents:
    """Tests for agent creation."""
    
    @pytest.mark.skipif(
        not pytest.importorskip("os").environ.get("OPENAI_API_KEY"),
        reason="OPENAI_API_KEY not set"
    )
    def test_schema_analyst_agent_creation(self):
        """Test schema analyst agent can be created."""
        from creatio_crm_crew.agents import SchemaAnalystAgent
        
        agent = SchemaAnalystAgent.create(tools=[])
        
        assert agent is not None
        assert "Schema" in agent.role or "Creatio" in agent.role
    
    @pytest.mark.skipif(
        not pytest.importorskip("os").environ.get("OPENAI_API_KEY"),
        reason="OPENAI_API_KEY not set"
    )
    def test_data_architect_agent_creation(self):
        """Test data architect agent can be created."""
        from creatio_crm_crew.agents import DataArchitectAgent
        
        agent = DataArchitectAgent.create(tools=[])
        
        assert agent is not None
        assert "Architect" in agent.role or "Creatio" in agent.role
    
    @pytest.mark.skipif(
        not pytest.importorskip("os").environ.get("OPENAI_API_KEY"),
        reason="OPENAI_API_KEY not set"
    )
    def test_metrics_expert_agent_creation(self):
        """Test metrics expert agent can be created."""
        from creatio_crm_crew.agents import MetricsExpertAgent
        
        agent = MetricsExpertAgent.create(tools=[])
        
        assert agent is not None
        assert "Metrics" in agent.role or "Analytics" in agent.role
    
    @pytest.mark.skipif(
        not pytest.importorskip("os").environ.get("OPENAI_API_KEY"),
        reason="OPENAI_API_KEY not set"
    )
    def test_query_builder_agent_creation(self):
        """Test query builder agent can be created."""
        from creatio_crm_crew.agents import QueryBuilderAgent
        
        agent = QueryBuilderAgent.create(tools=[])
        
        assert agent is not None
        assert "Query" in agent.role or "Creatio" in agent.role


class TestTasks:
    """Tests for task creation."""
    
    @pytest.mark.skipif(
        not pytest.importorskip("os").environ.get("OPENAI_API_KEY"),
        reason="OPENAI_API_KEY not set"
    )
    def test_schema_exploration_task(self):
        """Test schema exploration task creation."""
        from creatio_crm_crew.tasks import SchemaAnalysisTasks
        from creatio_crm_crew.agents import SchemaAnalystAgent
        
        agent = SchemaAnalystAgent.create(tools=[])
        task = SchemaAnalysisTasks.explore_entity(agent, "Contact")
        
        assert task is not None
        assert "Contact" in task.description
    
    @pytest.mark.skipif(
        not pytest.importorskip("os").environ.get("OPENAI_API_KEY"),
        reason="OPENAI_API_KEY not set"
    )
    def test_query_building_task(self):
        """Test query building task creation."""
        from creatio_crm_crew.tasks import QueryTasks
        from creatio_crm_crew.agents import QueryBuilderAgent
        
        agent = QueryBuilderAgent.create(tools=[])
        task = QueryTasks.build_query_from_question(agent, "Get all contacts")
        
        assert task is not None
        assert "contacts" in task.description.lower()
    
    @pytest.mark.skipif(
        not pytest.importorskip("os").environ.get("OPENAI_API_KEY"),
        reason="OPENAI_API_KEY not set"
    )
    def test_metrics_task(self):
        """Test metrics task creation."""
        from creatio_crm_crew.tasks import MetricsTasks
        from creatio_crm_crew.agents import MetricsExpertAgent
        
        agent = MetricsExpertAgent.create(tools=[])
        task = MetricsTasks.define_kpi(agent, "Sales performance", "B2B company")
        
        assert task is not None
        assert "Sales" in task.description or "KPI" in task.description
    
    @pytest.mark.skipif(
        not pytest.importorskip("os").environ.get("OPENAI_API_KEY"),
        reason="OPENAI_API_KEY not set"
    )
    def test_documentation_task(self):
        """Test documentation task creation."""
        from creatio_crm_crew.tasks import DocumentationTasks
        from creatio_crm_crew.agents import DataArchitectAgent
        
        agent = DataArchitectAgent.create(tools=[])
        task = DocumentationTasks.generate_entity_documentation(agent, "Contact")
        
        assert task is not None
        assert "Contact" in task.description


class TestCrewInitialization:
    """Tests for crew initialization."""
    
    @pytest.mark.skipif(
        not pytest.importorskip("os").environ.get("OPENAI_API_KEY"),
        reason="OPENAI_API_KEY not set"
    )
    def test_crew_initialization(self):
        """Test that crew can be initialized."""
        from creatio_crm_crew import CreatioCRMCrew
        
        crew = CreatioCRMCrew(verbose=False)
        
        assert crew is not None
        assert crew.schema_analyst is not None
        assert crew.data_architect is not None
        assert crew.metrics_expert is not None
        assert crew.query_builder is not None
    
    @pytest.mark.skipif(
        not pytest.importorskip("os").environ.get("OPENAI_API_KEY"),
        reason="OPENAI_API_KEY not set"
    )
    def test_crew_has_tools(self):
        """Test that crew has all tools initialized."""
        from creatio_crm_crew import CreatioCRMCrew
        
        crew = CreatioCRMCrew(verbose=False)
        
        assert len(crew.schema_tools) > 0
        assert len(crew.query_tools) > 0
        assert len(crew.metrics_tools) > 0
        assert len(crew.documentation_tools) > 0


class TestSchemaKnowledge:
    """Tests for schema knowledge base."""
    
    def test_schema_knowledge_has_core_entities(self):
        """Test that schema knowledge has core entities."""
        from creatio_crm_crew.tools.schema_tools import CREATIO_SCHEMA_KNOWLEDGE
        
        core_entities = ["Contact", "Account", "Opportunity", "Lead", "Activity", "Case"]
        
        for entity in core_entities:
            assert entity in CREATIO_SCHEMA_KNOWLEDGE
    
    def test_entity_has_required_fields(self):
        """Test that entities have required fields."""
        from creatio_crm_crew.tools.schema_tools import CREATIO_SCHEMA_KNOWLEDGE
        
        for entity_name, entity_info in CREATIO_SCHEMA_KNOWLEDGE.items():
            assert "description" in entity_info
            assert "table_name" in entity_info
            assert "key_columns" in entity_info
            assert len(entity_info["key_columns"]) > 0


class TestKPILibrary:
    """Tests for KPI library."""
    
    def test_kpi_library_has_categories(self):
        """Test that KPI library has expected categories."""
        from creatio_crm_crew.tools.metrics_tools import CRM_KPI_LIBRARY
        
        expected_categories = ["sales", "marketing", "customer_service"]
        
        for category in expected_categories:
            assert category in CRM_KPI_LIBRARY
    
    def test_kpi_has_required_fields(self):
        """Test that KPIs have required fields."""
        from creatio_crm_crew.tools.metrics_tools import CRM_KPI_LIBRARY
        
        for category, kpis in CRM_KPI_LIBRARY.items():
            for kpi_name, kpi_info in kpis.items():
                assert "name" in kpi_info
                assert "description" in kpi_info
                assert "formula" in kpi_info
                assert "unit" in kpi_info
                assert "entities" in kpi_info
