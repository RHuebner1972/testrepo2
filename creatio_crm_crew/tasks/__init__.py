"""Tasks module for Creatio CRM Crew."""

from creatio_crm_crew.tasks.schema_tasks import SchemaAnalysisTasks
from creatio_crm_crew.tasks.query_tasks import QueryTasks
from creatio_crm_crew.tasks.metrics_tasks import MetricsTasks
from creatio_crm_crew.tasks.documentation_tasks import DocumentationTasks

__all__ = [
    "SchemaAnalysisTasks",
    "QueryTasks",
    "MetricsTasks",
    "DocumentationTasks",
]
