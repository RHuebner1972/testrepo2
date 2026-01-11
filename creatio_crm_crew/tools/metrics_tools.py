"""
Metrics and KPI tools for Creatio CRM analytics.
"""

from typing import Type, Optional, List, Dict, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


# Comprehensive KPI library for CRM analytics
CRM_KPI_LIBRARY = {
    "sales": {
        "pipeline_value": {
            "name": "Pipeline Value",
            "description": "Total value of open opportunities in the sales pipeline",
            "formula": "SUM(Opportunity.Amount) WHERE Opportunity.Stage.IsFinal = 0",
            "unit": "currency",
            "frequency": "daily",
            "entities": ["Opportunity", "OpportunityStage"]
        },
        "win_rate": {
            "name": "Win Rate",
            "description": "Percentage of opportunities closed as won",
            "formula": "(COUNT(Won Opportunities) / COUNT(All Closed Opportunities)) * 100",
            "unit": "percentage",
            "frequency": "monthly",
            "entities": ["Opportunity", "OpportunityStage"]
        },
        "average_deal_size": {
            "name": "Average Deal Size",
            "description": "Average value of closed-won opportunities",
            "formula": "AVG(Opportunity.Amount) WHERE Stage.Name = 'Closed won'",
            "unit": "currency",
            "frequency": "monthly",
            "entities": ["Opportunity"]
        },
        "sales_cycle_length": {
            "name": "Sales Cycle Length",
            "description": "Average days from opportunity creation to close",
            "formula": "AVG(DATEDIFF(day, Opportunity.CreatedOn, Opportunity.CloseDate))",
            "unit": "days",
            "frequency": "monthly",
            "entities": ["Opportunity"]
        },
        "lead_conversion_rate": {
            "name": "Lead Conversion Rate",
            "description": "Percentage of leads converted to opportunities",
            "formula": "(COUNT(Converted Leads) / COUNT(All Leads)) * 100",
            "unit": "percentage",
            "frequency": "monthly",
            "entities": ["Lead"]
        },
        "revenue_by_rep": {
            "name": "Revenue by Sales Rep",
            "description": "Total closed revenue per sales representative",
            "formula": "SUM(Opportunity.Amount) GROUP BY OwnerId WHERE Stage = 'Closed won'",
            "unit": "currency",
            "frequency": "monthly",
            "entities": ["Opportunity", "Contact"]
        },
        "quota_attainment": {
            "name": "Quota Attainment",
            "description": "Percentage of sales quota achieved",
            "formula": "(Actual Revenue / Target Quota) * 100",
            "unit": "percentage",
            "frequency": "monthly",
            "entities": ["Opportunity", "SalesTarget"]
        },
        "opportunity_velocity": {
            "name": "Opportunity Velocity",
            "description": "Rate at which opportunities move through pipeline",
            "formula": "(# Opportunities * Win Rate * Avg Deal) / Sales Cycle",
            "unit": "currency/day",
            "frequency": "monthly",
            "entities": ["Opportunity"]
        }
    },
    "marketing": {
        "lead_volume": {
            "name": "Lead Volume",
            "description": "Number of new leads created in period",
            "formula": "COUNT(Lead) WHERE CreatedOn IN period",
            "unit": "count",
            "frequency": "weekly",
            "entities": ["Lead"]
        },
        "lead_source_effectiveness": {
            "name": "Lead Source Effectiveness",
            "description": "Leads and conversions by source",
            "formula": "COUNT(Lead) GROUP BY LeadSourceId",
            "unit": "count",
            "frequency": "monthly",
            "entities": ["Lead", "LeadSource"]
        },
        "marketing_qualified_leads": {
            "name": "Marketing Qualified Leads (MQL)",
            "description": "Leads meeting marketing qualification criteria",
            "formula": "COUNT(Lead) WHERE QualifyStatus = 'Marketing Qualified'",
            "unit": "count",
            "frequency": "weekly",
            "entities": ["Lead", "QualifyStatus"]
        },
        "cost_per_lead": {
            "name": "Cost Per Lead",
            "description": "Marketing spend divided by leads generated",
            "formula": "Marketing Spend / COUNT(Leads)",
            "unit": "currency",
            "frequency": "monthly",
            "entities": ["Lead", "Campaign"]
        },
        "campaign_roi": {
            "name": "Campaign ROI",
            "description": "Return on investment for marketing campaigns",
            "formula": "((Revenue - Cost) / Cost) * 100",
            "unit": "percentage",
            "frequency": "per_campaign",
            "entities": ["Campaign", "Opportunity"]
        }
    },
    "customer_service": {
        "case_volume": {
            "name": "Case Volume",
            "description": "Total number of support cases",
            "formula": "COUNT(Case)",
            "unit": "count",
            "frequency": "daily",
            "entities": ["Case"]
        },
        "average_resolution_time": {
            "name": "Average Resolution Time",
            "description": "Average time to resolve cases",
            "formula": "AVG(DATEDIFF(hour, Case.RegisteredOn, Case.SolutionDate))",
            "unit": "hours",
            "frequency": "weekly",
            "entities": ["Case"]
        },
        "first_response_time": {
            "name": "First Response Time",
            "description": "Average time to first response on cases",
            "formula": "AVG(DATEDIFF(minute, Case.RegisteredOn, FirstActivity.StartDate))",
            "unit": "minutes",
            "frequency": "daily",
            "entities": ["Case", "Activity"]
        },
        "customer_satisfaction": {
            "name": "Customer Satisfaction (CSAT)",
            "description": "Average satisfaction score from case surveys",
            "formula": "AVG(Case.SatisfactionLevel.Score)",
            "unit": "score",
            "frequency": "weekly",
            "entities": ["Case", "SatisfactionLevel"]
        },
        "sla_compliance": {
            "name": "SLA Compliance Rate",
            "description": "Percentage of cases resolved within SLA",
            "formula": "(COUNT(Cases within SLA) / COUNT(All Cases)) * 100",
            "unit": "percentage",
            "frequency": "weekly",
            "entities": ["Case", "ServicePact"]
        },
        "case_backlog": {
            "name": "Case Backlog",
            "description": "Number of open unresolved cases",
            "formula": "COUNT(Case) WHERE Status.IsFinal = 0",
            "unit": "count",
            "frequency": "daily",
            "entities": ["Case", "CaseStatus"]
        },
        "escalation_rate": {
            "name": "Escalation Rate",
            "description": "Percentage of cases that required escalation",
            "formula": "(COUNT(Escalated Cases) / COUNT(All Cases)) * 100",
            "unit": "percentage",
            "frequency": "weekly",
            "entities": ["Case"]
        }
    },
    "customer_health": {
        "customer_lifetime_value": {
            "name": "Customer Lifetime Value (CLV)",
            "description": "Total revenue expected from a customer relationship",
            "formula": "AVG Revenue per Period * Customer Lifespan",
            "unit": "currency",
            "frequency": "quarterly",
            "entities": ["Account", "Order", "Opportunity"]
        },
        "churn_rate": {
            "name": "Churn Rate",
            "description": "Percentage of customers lost in period",
            "formula": "(Lost Customers / Total Customers at Start) * 100",
            "unit": "percentage",
            "frequency": "monthly",
            "entities": ["Account"]
        },
        "net_promoter_score": {
            "name": "Net Promoter Score (NPS)",
            "description": "Customer loyalty and satisfaction metric",
            "formula": "% Promoters - % Detractors",
            "unit": "score",
            "frequency": "quarterly",
            "entities": ["Contact", "Survey"]
        },
        "customer_engagement_score": {
            "name": "Customer Engagement Score",
            "description": "Composite score of customer interaction levels",
            "formula": "Weighted sum of activities, responses, purchases",
            "unit": "score",
            "frequency": "monthly",
            "entities": ["Account", "Activity", "Opportunity"]
        },
        "revenue_retention": {
            "name": "Revenue Retention Rate",
            "description": "Percentage of revenue retained from existing customers",
            "formula": "((End Revenue - New Revenue) / Start Revenue) * 100",
            "unit": "percentage",
            "frequency": "monthly",
            "entities": ["Account", "Order"]
        }
    },
    "activity_metrics": {
        "activities_per_rep": {
            "name": "Activities per Rep",
            "description": "Number of activities logged per sales rep",
            "formula": "COUNT(Activity) GROUP BY OwnerId",
            "unit": "count",
            "frequency": "weekly",
            "entities": ["Activity", "Contact"]
        },
        "calls_made": {
            "name": "Calls Made",
            "description": "Number of call activities completed",
            "formula": "COUNT(Activity) WHERE Type = 'Call'",
            "unit": "count",
            "frequency": "daily",
            "entities": ["Activity", "ActivityType"]
        },
        "emails_sent": {
            "name": "Emails Sent",
            "description": "Number of email activities",
            "formula": "COUNT(Activity) WHERE Type = 'Email'",
            "unit": "count",
            "frequency": "daily",
            "entities": ["Activity", "ActivityType"]
        },
        "meetings_held": {
            "name": "Meetings Held",
            "description": "Number of meeting activities completed",
            "formula": "COUNT(Activity) WHERE Type = 'Meeting' AND Status = 'Completed'",
            "unit": "count",
            "frequency": "weekly",
            "entities": ["Activity", "ActivityType", "ActivityStatus"]
        }
    }
}


class MetricDefinitionInput(BaseModel):
    """Input schema for metric definition."""
    metric_name: str = Field(description="Name or description of the metric to define")
    business_context: str = Field(description="Business context or use case for the metric")
    target_entity: Optional[str] = Field(default=None, description="Primary entity the metric applies to")


class MetricCalculatorInput(BaseModel):
    """Input schema for metric calculation."""
    metric_id: str = Field(description="Identifier of the metric from KPI library (e.g., sales.win_rate)")
    time_period: str = Field(default="last_month", description="Time period: today, last_week, last_month, last_quarter, ytd")
    group_by: Optional[str] = Field(default=None, description="Optional grouping dimension")


class KPILibraryInput(BaseModel):
    """Input schema for KPI library queries."""
    category: Optional[str] = Field(default=None, description="Category to filter: sales, marketing, customer_service, customer_health, activity_metrics")
    search_term: Optional[str] = Field(default=None, description="Search term to find relevant KPIs")


class DashboardDesignInput(BaseModel):
    """Input schema for dashboard design."""
    dashboard_purpose: str = Field(description="Purpose of the dashboard (e.g., sales performance, executive overview)")
    audience: str = Field(description="Target audience: executive, manager, analyst, rep")
    key_questions: str = Field(description="Key business questions the dashboard should answer")


class MetricDefinitionTool(BaseTool):
    """Tool for defining custom metrics for Creatio CRM."""
    
    name: str = "metric_definition"
    description: str = (
        "Helps define and specify metrics/KPIs for Creatio CRM data. "
        "Creates detailed metric specifications including formulas, "
        "data sources, and calculation methods."
    )
    args_schema: Type[BaseModel] = MetricDefinitionInput
    
    def _run(
        self,
        metric_name: str,
        business_context: str,
        target_entity: Optional[str] = None
    ) -> str:
        """Define a metric."""
        # Analyze the metric request
        metric_lower = metric_name.lower()
        
        # Try to match with existing KPIs
        suggested_kpis = []
        for category, kpis in CRM_KPI_LIBRARY.items():
            for kpi_id, kpi_info in kpis.items():
                if (metric_lower in kpi_info["name"].lower() or 
                    metric_lower in kpi_info["description"].lower()):
                    suggested_kpis.append({
                        "id": f"{category}.{kpi_id}",
                        "name": kpi_info["name"],
                        "description": kpi_info["description"]
                    })
        
        # Create custom metric definition
        definition = {
            "success": True,
            "metric_request": metric_name,
            "business_context": business_context,
            "similar_existing_kpis": suggested_kpis[:5],
            "custom_definition": {
                "name": metric_name,
                "description": f"Custom metric for: {business_context}",
                "suggested_formula": self._suggest_formula(metric_name, target_entity),
                "data_requirements": self._identify_data_requirements(metric_name, target_entity),
                "calculation_frequency": self._suggest_frequency(metric_name),
                "visualization_type": self._suggest_visualization(metric_name),
            },
            "implementation_steps": [
                "1. Validate data availability in Creatio schema",
                "2. Create SQL query for data extraction",
                "3. Set up calculation schedule (if recurring)",
                "4. Add to dashboard or reporting system",
                "5. Define thresholds and alerts if needed"
            ]
        }
        
        return str(definition)
    
    def _suggest_formula(self, metric_name: str, entity: Optional[str]) -> str:
        """Suggest a formula based on metric name."""
        name_lower = metric_name.lower()
        
        if "rate" in name_lower or "percentage" in name_lower:
            return "(COUNT(matching_records) / COUNT(total_records)) * 100"
        if "average" in name_lower or "avg" in name_lower:
            return "AVG(column_name)"
        if "total" in name_lower or "sum" in name_lower:
            return "SUM(column_name)"
        if "count" in name_lower or "number" in name_lower:
            return "COUNT(records)"
        if "time" in name_lower or "duration" in name_lower:
            return "AVG(DATEDIFF(unit, start_date, end_date))"
        
        return "Define based on specific requirements"
    
    def _identify_data_requirements(self, metric_name: str, entity: Optional[str]) -> Dict[str, Any]:
        """Identify data requirements."""
        name_lower = metric_name.lower()
        requirements = {
            "primary_entity": entity or "To be determined",
            "required_columns": [],
            "related_entities": [],
            "filters_needed": []
        }
        
        # Identify entities based on keywords
        if "opportunity" in name_lower or "deal" in name_lower or "pipeline" in name_lower:
            requirements["primary_entity"] = "Opportunity"
            requirements["required_columns"] = ["Amount", "StageId", "CloseDate", "OwnerId"]
            requirements["related_entities"] = ["OpportunityStage", "Account"]
        elif "lead" in name_lower:
            requirements["primary_entity"] = "Lead"
            requirements["required_columns"] = ["QualifyStatusId", "LeadSourceId", "CreatedOn"]
            requirements["related_entities"] = ["QualifyStatus", "LeadSource"]
        elif "case" in name_lower or "ticket" in name_lower or "support" in name_lower:
            requirements["primary_entity"] = "Case"
            requirements["required_columns"] = ["StatusId", "RegisteredOn", "SolutionDate"]
            requirements["related_entities"] = ["CaseStatus", "SatisfactionLevel"]
        elif "activity" in name_lower or "call" in name_lower or "meeting" in name_lower:
            requirements["primary_entity"] = "Activity"
            requirements["required_columns"] = ["TypeId", "StatusId", "StartDate", "OwnerId"]
            requirements["related_entities"] = ["ActivityType", "ActivityStatus"]
        
        return requirements
    
    def _suggest_frequency(self, metric_name: str) -> str:
        """Suggest calculation frequency."""
        name_lower = metric_name.lower()
        
        if "daily" in name_lower or "today" in name_lower:
            return "daily"
        if "weekly" in name_lower:
            return "weekly"
        if "monthly" in name_lower:
            return "monthly"
        if "quarterly" in name_lower:
            return "quarterly"
        if "year" in name_lower or "annual" in name_lower:
            return "yearly"
        
        # Default based on metric type
        if "rate" in name_lower or "percentage" in name_lower:
            return "monthly"
        
        return "weekly"
    
    def _suggest_visualization(self, metric_name: str) -> str:
        """Suggest visualization type."""
        name_lower = metric_name.lower()
        
        if "trend" in name_lower or "over time" in name_lower:
            return "line_chart"
        if "by" in name_lower or "breakdown" in name_lower:
            return "bar_chart"
        if "distribution" in name_lower:
            return "pie_chart"
        if "rate" in name_lower or "percentage" in name_lower:
            return "gauge"
        if "comparison" in name_lower:
            return "bar_chart"
        
        return "single_value_card"


class MetricCalculatorTool(BaseTool):
    """Tool for calculating metrics from Creatio CRM data."""
    
    name: str = "metric_calculator"
    description: str = (
        "Calculates specific KPIs and metrics from Creatio CRM data. "
        "Generates the SQL query needed to compute the metric "
        "and provides sample calculations."
    )
    args_schema: Type[BaseModel] = MetricCalculatorInput
    
    def _run(
        self,
        metric_id: str,
        time_period: str = "last_month",
        group_by: Optional[str] = None
    ) -> str:
        """Calculate a metric."""
        # Parse metric ID
        parts = metric_id.split(".")
        if len(parts) != 2:
            return str({
                "success": False,
                "error": f"Invalid metric_id format. Use 'category.metric_name' (e.g., 'sales.win_rate')",
                "available_categories": list(CRM_KPI_LIBRARY.keys())
            })
        
        category, metric_name = parts
        
        if category not in CRM_KPI_LIBRARY:
            return str({
                "success": False,
                "error": f"Unknown category: {category}",
                "available_categories": list(CRM_KPI_LIBRARY.keys())
            })
        
        if metric_name not in CRM_KPI_LIBRARY[category]:
            return str({
                "success": False,
                "error": f"Unknown metric: {metric_name}",
                "available_metrics": list(CRM_KPI_LIBRARY[category].keys())
            })
        
        kpi = CRM_KPI_LIBRARY[category][metric_name]
        
        # Generate SQL query
        sql_query = self._generate_calculation_query(kpi, time_period, group_by)
        
        # Generate date filter based on time period
        date_filter = self._get_date_filter(time_period)
        
        result = {
            "success": True,
            "metric": {
                "id": metric_id,
                "name": kpi["name"],
                "description": kpi["description"],
                "unit": kpi["unit"]
            },
            "calculation": {
                "formula": kpi["formula"],
                "sql_query": sql_query,
                "time_period": time_period,
                "date_filter": date_filter,
                "group_by": group_by
            },
            "entities_required": kpi["entities"],
            "notes": [
                f"Recommended calculation frequency: {kpi['frequency']}",
                "Ensure appropriate indexes exist for date columns",
                "Consider caching results for dashboard performance"
            ]
        }
        
        return str(result)
    
    def _generate_calculation_query(self, kpi: Dict, time_period: str, group_by: Optional[str]) -> str:
        """Generate SQL query for metric calculation."""
        primary_entity = kpi["entities"][0]
        date_filter = self._get_date_filter(time_period)
        
        # Templates for common metrics
        if kpi["unit"] == "percentage" and "rate" in kpi["name"].lower():
            if "win" in kpi["name"].lower():
                return f"""
SELECT 
    CAST(SUM(CASE WHEN s.Name = 'Closed won' THEN 1 ELSE 0 END) AS FLOAT) /
    NULLIF(COUNT(*), 0) * 100 AS WinRate
FROM [Opportunity] o
JOIN [OpportunityStage] s ON o.StageId = s.Id
WHERE s.IsFinal = 1
    AND {date_filter}
"""
            if "conversion" in kpi["name"].lower():
                return f"""
SELECT 
    CAST(SUM(CASE WHEN QualifiedContactId IS NOT NULL THEN 1 ELSE 0 END) AS FLOAT) /
    NULLIF(COUNT(*), 0) * 100 AS ConversionRate
FROM [Lead]
WHERE {date_filter}
"""
        
        if kpi["unit"] == "currency":
            if "pipeline" in kpi["name"].lower():
                return f"""
SELECT SUM(o.Amount) AS PipelineValue
FROM [Opportunity] o
JOIN [OpportunityStage] s ON o.StageId = s.Id
WHERE s.IsFinal = 0
"""
            if "average" in kpi["name"].lower():
                return f"""
SELECT AVG(o.Amount) AS AverageDealSize
FROM [Opportunity] o
JOIN [OpportunityStage] s ON o.StageId = s.Id
WHERE s.Name = 'Closed won'
    AND {date_filter}
"""
        
        if kpi["unit"] == "days" or kpi["unit"] == "hours":
            return f"""
SELECT AVG(DATEDIFF({kpi['unit'][:-1]}, CreatedOn, CloseDate)) AS {kpi['name'].replace(' ', '')}
FROM [{primary_entity}]
WHERE {date_filter}
"""
        
        # Default count query
        return f"""
SELECT COUNT(*) AS {kpi['name'].replace(' ', '')}
FROM [{primary_entity}]
WHERE {date_filter}
"""
    
    def _get_date_filter(self, time_period: str) -> str:
        """Get SQL date filter for time period."""
        filters = {
            "today": "CAST(CreatedOn AS DATE) = CAST(GETDATE() AS DATE)",
            "last_week": "CreatedOn >= DATEADD(WEEK, -1, GETDATE())",
            "last_month": "CreatedOn >= DATEADD(MONTH, -1, GETDATE())",
            "last_quarter": "CreatedOn >= DATEADD(QUARTER, -1, GETDATE())",
            "ytd": "YEAR(CreatedOn) = YEAR(GETDATE())",
            "last_year": "CreatedOn >= DATEADD(YEAR, -1, GETDATE())",
        }
        return filters.get(time_period, filters["last_month"])


class KPILibraryTool(BaseTool):
    """Tool for browsing the KPI library."""
    
    name: str = "kpi_library"
    description: str = (
        "Browses the comprehensive KPI library for Creatio CRM. "
        "Search or filter KPIs by category to find relevant metrics "
        "for your business needs."
    )
    args_schema: Type[BaseModel] = KPILibraryInput
    
    def _run(
        self,
        category: Optional[str] = None,
        search_term: Optional[str] = None
    ) -> str:
        """Browse KPI library."""
        results = {
            "success": True,
            "filter": {
                "category": category,
                "search_term": search_term
            },
            "kpis": []
        }
        
        # Filter by category
        categories_to_search = [category] if category else CRM_KPI_LIBRARY.keys()
        
        for cat in categories_to_search:
            if cat not in CRM_KPI_LIBRARY:
                continue
            
            for kpi_id, kpi_info in CRM_KPI_LIBRARY[cat].items():
                # Apply search filter
                if search_term:
                    term_lower = search_term.lower()
                    if (term_lower not in kpi_info["name"].lower() and
                        term_lower not in kpi_info["description"].lower()):
                        continue
                
                results["kpis"].append({
                    "id": f"{cat}.{kpi_id}",
                    "category": cat,
                    "name": kpi_info["name"],
                    "description": kpi_info["description"],
                    "unit": kpi_info["unit"],
                    "frequency": kpi_info["frequency"]
                })
        
        results["summary"] = {
            "total_kpis_found": len(results["kpis"]),
            "categories_searched": list(categories_to_search),
            "available_categories": list(CRM_KPI_LIBRARY.keys())
        }
        
        return str(results)


class DashboardDesignerTool(BaseTool):
    """Tool for designing dashboards from Creatio CRM metrics."""
    
    name: str = "dashboard_designer"
    description: str = (
        "Helps design dashboards for Creatio CRM data visualization. "
        "Recommends KPIs, layouts, and visualizations based on "
        "the dashboard purpose and target audience."
    )
    args_schema: Type[BaseModel] = DashboardDesignInput
    
    def _run(
        self,
        dashboard_purpose: str,
        audience: str,
        key_questions: str
    ) -> str:
        """Design a dashboard."""
        # Analyze purpose to suggest KPIs
        purpose_lower = dashboard_purpose.lower()
        
        recommended_kpis = []
        
        if "sales" in purpose_lower or "revenue" in purpose_lower:
            recommended_kpis.extend([
                "sales.pipeline_value",
                "sales.win_rate",
                "sales.average_deal_size",
                "sales.sales_cycle_length",
                "sales.revenue_by_rep"
            ])
        
        if "marketing" in purpose_lower or "lead" in purpose_lower:
            recommended_kpis.extend([
                "marketing.lead_volume",
                "marketing.lead_conversion_rate",
                "marketing.lead_source_effectiveness",
                "marketing.marketing_qualified_leads"
            ])
        
        if "service" in purpose_lower or "support" in purpose_lower or "case" in purpose_lower:
            recommended_kpis.extend([
                "customer_service.case_volume",
                "customer_service.average_resolution_time",
                "customer_service.customer_satisfaction",
                "customer_service.sla_compliance"
            ])
        
        if "executive" in purpose_lower or "overview" in purpose_lower:
            recommended_kpis = [
                "sales.pipeline_value",
                "sales.win_rate",
                "marketing.lead_conversion_rate",
                "customer_service.customer_satisfaction",
                "customer_health.revenue_retention"
            ]
        
        # Determine layout based on audience
        layout_config = {
            "executive": {
                "style": "high-level summary",
                "max_widgets": 6,
                "widget_types": ["scorecard", "trend_line", "gauge"],
                "refresh_frequency": "daily"
            },
            "manager": {
                "style": "operational overview",
                "max_widgets": 10,
                "widget_types": ["scorecard", "bar_chart", "table", "trend_line"],
                "refresh_frequency": "hourly"
            },
            "analyst": {
                "style": "detailed analysis",
                "max_widgets": 15,
                "widget_types": ["table", "pivot", "scatter", "heatmap", "drill-down"],
                "refresh_frequency": "real-time"
            },
            "rep": {
                "style": "personal performance",
                "max_widgets": 8,
                "widget_types": ["scorecard", "progress_bar", "activity_feed", "leaderboard"],
                "refresh_frequency": "real-time"
            }
        }
        
        audience_config = layout_config.get(audience.lower(), layout_config["manager"])
        
        design = {
            "success": True,
            "dashboard_purpose": dashboard_purpose,
            "target_audience": audience,
            "key_questions": key_questions,
            "design": {
                "layout_style": audience_config["style"],
                "recommended_widget_count": audience_config["max_widgets"],
                "widget_types": audience_config["widget_types"],
                "refresh_frequency": audience_config["refresh_frequency"]
            },
            "recommended_kpis": recommended_kpis[:8],
            "widget_recommendations": self._generate_widget_layout(recommended_kpis[:6], audience_config),
            "implementation_notes": [
                "Use Creatio's built-in dashboard designer for native integration",
                "Consider external BI tools (Power BI, Tableau) for advanced analytics",
                "Implement caching for complex calculations",
                "Set up scheduled data refresh for consistency"
            ],
            "data_requirements": {
                "entities_needed": list(set([
                    entity
                    for kpi_id in recommended_kpis[:8]
                    for entity in CRM_KPI_LIBRARY.get(kpi_id.split(".")[0], {}).get(kpi_id.split(".")[-1], {}).get("entities", [])
                    if "." in kpi_id
                ])),
                "estimated_query_complexity": "medium" if len(recommended_kpis) > 5 else "low"
            }
        }
        
        return str(design)
    
    def _generate_widget_layout(self, kpis: List[str], config: Dict) -> List[Dict]:
        """Generate widget layout suggestions."""
        widgets = []
        
        for i, kpi_id in enumerate(kpis):
            parts = kpi_id.split(".")
            if len(parts) != 2:
                continue
            
            category, metric = parts
            kpi_info = CRM_KPI_LIBRARY.get(category, {}).get(metric, {})
            
            if not kpi_info:
                continue
            
            # Determine widget type based on metric
            if kpi_info.get("unit") == "percentage":
                widget_type = "gauge"
            elif kpi_info.get("unit") == "currency":
                widget_type = "scorecard"
            elif kpi_info.get("unit") == "count":
                widget_type = "bar_chart" if i % 2 == 0 else "scorecard"
            else:
                widget_type = "trend_line"
            
            widgets.append({
                "position": i + 1,
                "kpi_id": kpi_id,
                "kpi_name": kpi_info.get("name", metric),
                "widget_type": widget_type,
                "size": "medium" if widget_type in ["bar_chart", "trend_line"] else "small",
                "show_trend": True if kpi_info.get("unit") in ["percentage", "currency", "count"] else False
            })
        
        return widgets
