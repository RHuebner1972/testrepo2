"""Tools module for Creatio CRM Crew."""

from creatio_crm_crew.tools.schema_tools import (
    SchemaExplorerTool,
    EntityRelationshipTool,
    ColumnAnalyzerTool,
    SchemaSearchTool,
)
from creatio_crm_crew.tools.query_tools import (
    SQLQueryBuilderTool,
    ODataQueryBuilderTool,
    QueryOptimizerTool,
    QueryValidatorTool,
)
from creatio_crm_crew.tools.metrics_tools import (
    MetricDefinitionTool,
    MetricCalculatorTool,
    KPILibraryTool,
    DashboardDesignerTool,
)
from creatio_crm_crew.tools.documentation_tools import (
    SchemaDocGeneratorTool,
    DataDictionaryTool,
    ERDGeneratorTool,
)

__all__ = [
    # Schema tools
    "SchemaExplorerTool",
    "EntityRelationshipTool",
    "ColumnAnalyzerTool",
    "SchemaSearchTool",
    # Query tools
    "SQLQueryBuilderTool",
    "ODataQueryBuilderTool",
    "QueryOptimizerTool",
    "QueryValidatorTool",
    # Metrics tools
    "MetricDefinitionTool",
    "MetricCalculatorTool",
    "KPILibraryTool",
    "DashboardDesignerTool",
    # Documentation tools
    "SchemaDocGeneratorTool",
    "DataDictionaryTool",
    "ERDGeneratorTool",
]
