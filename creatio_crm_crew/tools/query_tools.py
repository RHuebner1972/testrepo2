"""
Query building and optimization tools for Creatio CRM.
"""

from typing import Type, Optional, List
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class SQLQueryInput(BaseModel):
    """Input schema for SQL query building."""
    objective: str = Field(description="Business objective or question the query should answer")
    entities: str = Field(description="Comma-separated list of entities to include (e.g., Contact, Account)")
    filters: Optional[str] = Field(default=None, description="Filter conditions in natural language")
    aggregations: Optional[str] = Field(default=None, description="Aggregations needed (count, sum, avg, etc.)")
    grouping: Optional[str] = Field(default=None, description="Grouping columns")
    ordering: Optional[str] = Field(default=None, description="Sort order")


class ODataQueryInput(BaseModel):
    """Input schema for OData query building."""
    entity: str = Field(description="Primary entity to query")
    select_fields: Optional[str] = Field(default=None, description="Comma-separated fields to return")
    filter_expression: Optional[str] = Field(default=None, description="Filter in natural language")
    expand_relations: Optional[str] = Field(default=None, description="Related entities to expand")
    top: int = Field(default=100, description="Maximum records to return")


class QueryOptimizeInput(BaseModel):
    """Input schema for query optimization."""
    query: str = Field(description="SQL or OData query to optimize")
    query_type: str = Field(default="sql", description="Type of query: sql or odata")
    optimization_goal: str = Field(default="performance", description="Goal: performance, readability, both")


class QueryValidateInput(BaseModel):
    """Input schema for query validation."""
    query: str = Field(description="Query to validate")
    query_type: str = Field(default="sql", description="Type: sql or odata")


class SQLQueryBuilderTool(BaseTool):
    """Tool for building SQL queries for Creatio CRM."""
    
    name: str = "sql_query_builder"
    description: str = (
        "Builds SQL queries for extracting data from Creatio CRM database. "
        "Translates business questions into well-structured SQL with proper "
        "joins, filters, and aggregations based on Creatio's schema."
    )
    args_schema: Type[BaseModel] = SQLQueryInput
    
    def _run(
        self,
        objective: str,
        entities: str,
        filters: Optional[str] = None,
        aggregations: Optional[str] = None,
        grouping: Optional[str] = None,
        ordering: Optional[str] = None
    ) -> str:
        """Build SQL query."""
        entity_list = [e.strip() for e in entities.split(",")]
        primary_entity = entity_list[0]
        
        # Build query components
        select_clause = self._build_select(primary_entity, entity_list, aggregations)
        from_clause = self._build_from(entity_list)
        where_clause = self._build_where(filters) if filters else ""
        group_clause = self._build_group(grouping) if grouping else ""
        order_clause = self._build_order(ordering) if ordering else ""
        
        # Assemble query
        query_parts = [select_clause, from_clause]
        if where_clause:
            query_parts.append(where_clause)
        if group_clause:
            query_parts.append(group_clause)
        if order_clause:
            query_parts.append(order_clause)
        
        query = "\n".join(query_parts) + ";"
        
        result = {
            "success": True,
            "objective": objective,
            "query": query,
            "entities_used": entity_list,
            "query_type": "SELECT",
            "has_aggregation": aggregations is not None,
            "has_grouping": grouping is not None,
            "explanation": self._explain_query(primary_entity, entity_list, filters, aggregations),
            "performance_notes": [
                "Consider adding indexes on filter columns",
                "Use date range filters to limit result set",
                "Add TOP clause for testing with large datasets"
            ]
        }
        
        return str(result)
    
    def _build_select(self, primary: str, entities: List[str], aggregations: Optional[str]) -> str:
        """Build SELECT clause."""
        if aggregations:
            agg_funcs = {
                "count": f"COUNT({primary}.Id) AS RecordCount",
                "sum": f"SUM({primary}.Amount) AS TotalAmount",
                "avg": f"AVG({primary}.Amount) AS AvgAmount",
            }
            agg_lower = aggregations.lower()
            agg_cols = []
            for key, val in agg_funcs.items():
                if key in agg_lower:
                    agg_cols.append(val)
            if agg_cols:
                return f"SELECT\n    {', '.join(agg_cols)}"
        
        # Default columns based on entity
        default_cols = {
            "Contact": ["c.Id", "c.Name", "c.Email", "c.Phone", "c.AccountId"],
            "Account": ["a.Id", "a.Name", "a.Phone", "a.Web", "a.IndustryId"],
            "Opportunity": ["o.Id", "o.Title", "o.Amount", "o.StageId", "o.CloseDate"],
            "Lead": ["l.Id", "l.LeadName", "l.Email", "l.QualifyStatusId"],
            "Activity": ["act.Id", "act.Title", "act.TypeId", "act.StartDate"],
            "Case": ["cs.Id", "cs.Number", "cs.Subject", "cs.StatusId"],
        }
        
        cols = default_cols.get(primary, [f"{primary[0].lower()}.Id", f"{primary[0].lower()}.Name"])
        return f"SELECT\n    {',\n    '.join(cols)}"
    
    def _build_from(self, entities: List[str]) -> str:
        """Build FROM clause with JOINs."""
        aliases = {"Contact": "c", "Account": "a", "Opportunity": "o", "Lead": "l", 
                   "Activity": "act", "Case": "cs", "Product": "p", "Order": "ord"}
        
        primary = entities[0]
        alias = aliases.get(primary, primary[0].lower())
        from_clause = f"FROM [{primary}] {alias}"
        
        # Add joins for additional entities
        join_templates = {
            ("Contact", "Account"): "LEFT JOIN [Account] a ON c.AccountId = a.Id",
            ("Account", "Contact"): "LEFT JOIN [Contact] c ON c.AccountId = a.Id",
            ("Opportunity", "Account"): "LEFT JOIN [Account] a ON o.AccountId = a.Id",
            ("Activity", "Contact"): "LEFT JOIN [Contact] c ON act.ContactId = c.Id",
            ("Activity", "Account"): "LEFT JOIN [Account] a ON act.AccountId = a.Id",
            ("Case", "Contact"): "LEFT JOIN [Contact] c ON cs.ContactId = c.Id",
            ("Case", "Account"): "LEFT JOIN [Account] a ON cs.AccountId = a.Id",
            ("Lead", "Contact"): "LEFT JOIN [Contact] c ON l.QualifiedContactId = c.Id",
        }
        
        for entity in entities[1:]:
            join_key = (primary, entity)
            reverse_key = (entity, primary)
            
            if join_key in join_templates:
                from_clause += f"\n{join_templates[join_key]}"
            elif reverse_key in join_templates:
                from_clause += f"\n{join_templates[reverse_key]}"
            else:
                alias = aliases.get(entity, entity[0].lower())
                from_clause += f"\n-- Add JOIN for [{entity}] based on your relationship"
        
        return from_clause
    
    def _build_where(self, filters: str) -> str:
        """Build WHERE clause from natural language."""
        conditions = []
        filter_lower = filters.lower()
        
        # Parse common filter patterns
        if "this month" in filter_lower:
            conditions.append("CreatedOn >= DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0)")
        if "this quarter" in filter_lower:
            conditions.append("CreatedOn >= DATEADD(QUARTER, DATEDIFF(QUARTER, 0, GETDATE()), 0)")
        if "this year" in filter_lower:
            conditions.append("YEAR(CreatedOn) = YEAR(GETDATE())")
        if "active" in filter_lower:
            conditions.append("IsActive = 1")
        if "closed" in filter_lower:
            conditions.append("StatusId IN (SELECT Id FROM [OpportunityStatus] WHERE IsFinal = 1)")
        if "won" in filter_lower:
            conditions.append("StageId = (SELECT Id FROM [OpportunityStage] WHERE Name = 'Closed won')")
        
        if conditions:
            return "WHERE\n    " + "\n    AND ".join(conditions)
        
        return f"WHERE -- Add conditions based on: {filters}"
    
    def _build_group(self, grouping: str) -> str:
        """Build GROUP BY clause."""
        return f"GROUP BY {grouping}"
    
    def _build_order(self, ordering: str) -> str:
        """Build ORDER BY clause."""
        if "newest" in ordering.lower() or "recent" in ordering.lower():
            return "ORDER BY CreatedOn DESC"
        if "oldest" in ordering.lower():
            return "ORDER BY CreatedOn ASC"
        if "amount" in ordering.lower():
            return "ORDER BY Amount DESC"
        return f"ORDER BY {ordering}"
    
    def _explain_query(self, primary: str, entities: List[str], filters: Optional[str], aggregations: Optional[str]) -> str:
        """Generate query explanation."""
        explanation = f"This query retrieves data from {primary}"
        if len(entities) > 1:
            explanation += f" joined with {', '.join(entities[1:])}"
        if filters:
            explanation += f" filtered by: {filters}"
        if aggregations:
            explanation += f" with aggregations: {aggregations}"
        return explanation


class ODataQueryBuilderTool(BaseTool):
    """Tool for building OData queries for Creatio API."""
    
    name: str = "odata_query_builder"
    description: str = (
        "Builds OData queries for Creatio CRM REST API. "
        "Creates properly formatted $select, $filter, $expand, and $orderby clauses "
        "for API-based data retrieval."
    )
    args_schema: Type[BaseModel] = ODataQueryInput
    
    def _run(
        self,
        entity: str,
        select_fields: Optional[str] = None,
        filter_expression: Optional[str] = None,
        expand_relations: Optional[str] = None,
        top: int = 100
    ) -> str:
        """Build OData query."""
        base_url = f"/0/odata/{entity}Collection"
        query_params = []
        
        # Build $select
        if select_fields:
            fields = [f.strip() for f in select_fields.split(",")]
            query_params.append(f"$select={','.join(fields)}")
        
        # Build $filter
        if filter_expression:
            odata_filter = self._convert_to_odata_filter(filter_expression, entity)
            query_params.append(f"$filter={odata_filter}")
        
        # Build $expand
        if expand_relations:
            relations = [r.strip() for r in expand_relations.split(",")]
            expand_clause = ",".join(relations)
            query_params.append(f"$expand={expand_clause}")
        
        # Add $top
        query_params.append(f"$top={top}")
        
        # Assemble URL
        if query_params:
            full_url = base_url + "?" + "&".join(query_params)
        else:
            full_url = base_url
        
        result = {
            "success": True,
            "entity": entity,
            "odata_url": full_url,
            "query_parts": {
                "base": base_url,
                "select": select_fields,
                "filter": filter_expression,
                "expand": expand_relations,
                "top": top
            },
            "curl_example": self._generate_curl(full_url),
            "usage_notes": [
                "Add authentication headers (BPMCSRF token)",
                "Use $skip for pagination",
                "Add $count=true to get total count"
            ]
        }
        
        return str(result)
    
    def _convert_to_odata_filter(self, natural_filter: str, entity: str) -> str:
        """Convert natural language filter to OData syntax."""
        filter_lower = natural_filter.lower()
        conditions = []
        
        # Date filters
        if "today" in filter_lower:
            conditions.append("CreatedOn ge cast(now(), Edm.DateTimeOffset)")
        if "this month" in filter_lower:
            conditions.append("month(CreatedOn) eq month(now()) and year(CreatedOn) eq year(now())")
        if "active" in filter_lower:
            conditions.append("IsActive eq true")
        
        # Status filters
        if "open" in filter_lower:
            if entity.lower() == "opportunity":
                conditions.append("Stage/IsFinal eq false")
            elif entity.lower() == "case":
                conditions.append("Status/IsFinal eq false")
        
        if conditions:
            return " and ".join(conditions)
        
        return f"/* Add filter for: {natural_filter} */"
    
    def _generate_curl(self, url: str) -> str:
        """Generate curl example."""
        return f'''curl -X GET "{{CREATIO_URL}}{url}" \\
  -H "Accept: application/json" \\
  -H "Content-Type: application/json" \\
  -H "BPMCSRF: {{csrf_token}}" \\
  --cookie "BPMCSRF={{csrf_token}};.ASPXAUTH={{auth_cookie}}"'''


class QueryOptimizerTool(BaseTool):
    """Tool for optimizing Creatio queries."""
    
    name: str = "query_optimizer"
    description: str = (
        "Analyzes and optimizes SQL or OData queries for better performance. "
        "Suggests indexing, query restructuring, and best practices."
    )
    args_schema: Type[BaseModel] = QueryOptimizeInput
    
    def _run(
        self,
        query: str,
        query_type: str = "sql",
        optimization_goal: str = "performance"
    ) -> str:
        """Optimize a query."""
        analysis = {
            "success": True,
            "original_query": query,
            "query_type": query_type,
            "optimization_goal": optimization_goal,
            "issues_found": [],
            "recommendations": [],
            "optimized_query": query
        }
        
        query_lower = query.lower()
        
        # Analyze for common issues
        if query_type == "sql":
            # Check for SELECT *
            if "select *" in query_lower:
                analysis["issues_found"].append({
                    "severity": "high",
                    "issue": "Using SELECT * returns unnecessary columns",
                    "fix": "Specify only needed columns"
                })
                analysis["recommendations"].append("Replace SELECT * with specific columns")
            
            # Check for missing WHERE clause
            if "where" not in query_lower and "group by" not in query_lower:
                analysis["issues_found"].append({
                    "severity": "high",
                    "issue": "Query has no WHERE clause - will scan entire table",
                    "fix": "Add appropriate filter conditions"
                })
            
            # Check for missing TOP/LIMIT
            if "top" not in query_lower and "limit" not in query_lower:
                analysis["issues_found"].append({
                    "severity": "medium",
                    "issue": "No row limit specified",
                    "fix": "Add TOP or LIMIT clause for testing"
                })
                analysis["recommendations"].append("Add TOP 1000 during development")
            
            # Check for date range on CreatedOn
            if "createdon" in query_lower:
                if "between" not in query_lower and ">=" not in query_lower:
                    analysis["recommendations"].append("Consider adding date range filter on CreatedOn for better index usage")
            
            # Check for join efficiency
            if "join" in query_lower:
                analysis["recommendations"].append("Ensure join columns have appropriate indexes")
                analysis["recommendations"].append("Consider the order of joins - put most restrictive first")
            
            # Check for function on columns
            functions_on_cols = ["year(", "month(", "day(", "datepart("]
            for func in functions_on_cols:
                if func in query_lower:
                    analysis["issues_found"].append({
                        "severity": "medium",
                        "issue": f"Function {func.upper()} on column prevents index usage",
                        "fix": "Use range comparison instead of function extraction"
                    })
        
        elif query_type == "odata":
            # OData specific optimizations
            if "$select" not in query_lower:
                analysis["issues_found"].append({
                    "severity": "medium",
                    "issue": "No $select - returning all columns",
                    "fix": "Add $select with only needed fields"
                })
            
            if "$top" not in query_lower:
                analysis["recommendations"].append("Add $top for pagination")
            
            if "$expand" in query_lower and "$select" in query_lower:
                analysis["recommendations"].append("Consider using $select within $expand to limit expanded data")
        
        # Add index recommendations for common patterns
        if "accountid" in query_lower:
            analysis["recommendations"].append("Ensure index exists on AccountId column")
        if "createdon" in query_lower:
            analysis["recommendations"].append("Ensure index exists on CreatedOn column")
        if "ownerid" in query_lower:
            analysis["recommendations"].append("Ensure index exists on OwnerId column")
        
        analysis["optimization_summary"] = {
            "issues_count": len(analysis["issues_found"]),
            "recommendations_count": len(analysis["recommendations"]),
            "critical_issues": len([i for i in analysis["issues_found"] if i["severity"] == "high"])
        }
        
        return str(analysis)


class QueryValidatorTool(BaseTool):
    """Tool for validating Creatio queries."""
    
    name: str = "query_validator"
    description: str = (
        "Validates SQL or OData queries for syntax correctness "
        "and compatibility with Creatio CRM schema."
    )
    args_schema: Type[BaseModel] = QueryValidateInput
    
    def _run(self, query: str, query_type: str = "sql") -> str:
        """Validate a query."""
        validation = {
            "success": True,
            "query": query,
            "query_type": query_type,
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "entities_referenced": [],
            "columns_referenced": []
        }
        
        query_lower = query.lower()
        
        # Known Creatio entities
        known_entities = [
            "contact", "account", "opportunity", "lead", "activity",
            "case", "product", "order", "sysadminunit", "syslookup"
        ]
        
        # Check for entity references
        for entity in known_entities:
            if entity in query_lower or f"[{entity}]" in query_lower:
                validation["entities_referenced"].append(entity.capitalize())
        
        if query_type == "sql":
            # Basic SQL validation
            required_keywords = ["select"]
            for keyword in required_keywords:
                if keyword not in query_lower:
                    validation["is_valid"] = False
                    validation["errors"].append(f"Missing required keyword: {keyword.upper()}")
            
            # Check for balanced brackets
            if query.count("[") != query.count("]"):
                validation["is_valid"] = False
                validation["errors"].append("Unbalanced square brackets")
            
            if query.count("(") != query.count(")"):
                validation["is_valid"] = False
                validation["errors"].append("Unbalanced parentheses")
            
            # Check for common typos
            common_typos = [
                ("slect", "SELECT"),
                ("frmo", "FROM"),
                ("wehre", "WHERE"),
                ("gruop", "GROUP"),
                ("ordre", "ORDER"),
            ]
            for typo, correct in common_typos:
                if typo in query_lower:
                    validation["is_valid"] = False
                    validation["errors"].append(f"Possible typo: '{typo}' should be '{correct}'")
            
            # Warnings
            if "delete" in query_lower or "drop" in query_lower or "truncate" in query_lower:
                validation["warnings"].append("Query contains destructive operation - use with caution!")
            
            if "update" in query_lower and "where" not in query_lower:
                validation["warnings"].append("UPDATE without WHERE will affect all rows!")
        
        elif query_type == "odata":
            # OData validation
            if "/odata/" not in query and "Collection" not in query:
                validation["warnings"].append("OData URL should include /odata/ path and Collection suffix")
            
            # Check for valid query parameters
            valid_params = ["$select", "$filter", "$expand", "$orderby", "$top", "$skip", "$count"]
            for param in ["$select", "$filter", "$expand", "$orderby", "$top", "$skip"]:
                if param in query_lower:
                    # Check if it's properly formatted
                    if f"{param}=" not in query_lower and f"{param} =" not in query_lower:
                        validation["warnings"].append(f"{param} should be followed by = and value")
        
        validation["validation_summary"] = {
            "is_valid": validation["is_valid"],
            "error_count": len(validation["errors"]),
            "warning_count": len(validation["warnings"]),
            "entities_found": len(validation["entities_referenced"])
        }
        
        return str(validation)
