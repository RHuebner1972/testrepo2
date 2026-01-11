"""
Schema exploration and analysis tools for Creatio CRM.
"""

from typing import Type, Optional, List, Dict, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


# Creatio CRM Schema Knowledge Base
# This represents common Creatio CRM entities and their relationships
CREATIO_SCHEMA_KNOWLEDGE = {
    "Contact": {
        "description": "Core entity storing person/individual information",
        "table_name": "Contact",
        "key_columns": [
            {"name": "Id", "type": "uniqueidentifier", "description": "Primary key"},
            {"name": "Name", "type": "nvarchar(250)", "description": "Full name of the contact"},
            {"name": "AccountId", "type": "uniqueidentifier", "description": "FK to Account - associated company"},
            {"name": "Email", "type": "nvarchar(250)", "description": "Primary email address"},
            {"name": "Phone", "type": "nvarchar(250)", "description": "Primary phone number"},
            {"name": "MobilePhone", "type": "nvarchar(250)", "description": "Mobile phone number"},
            {"name": "JobTitle", "type": "nvarchar(250)", "description": "Contact's job title"},
            {"name": "DepartmentId", "type": "uniqueidentifier", "description": "FK to Department lookup"},
            {"name": "OwnerId", "type": "uniqueidentifier", "description": "FK to Contact - record owner"},
            {"name": "TypeId", "type": "uniqueidentifier", "description": "FK to ContactType lookup"},
            {"name": "CreatedOn", "type": "datetime", "description": "Record creation timestamp"},
            {"name": "ModifiedOn", "type": "datetime", "description": "Last modification timestamp"},
        ],
        "relationships": [
            {"entity": "Account", "type": "many-to-one", "column": "AccountId"},
            {"entity": "Activity", "type": "one-to-many", "detail": True},
            {"entity": "Opportunity", "type": "one-to-many", "via": "OpportunityContact"},
            {"entity": "Lead", "type": "one-to-one", "column": "QualifiedContactId"},
        ]
    },
    "Account": {
        "description": "Core entity storing company/organization information",
        "table_name": "Account",
        "key_columns": [
            {"name": "Id", "type": "uniqueidentifier", "description": "Primary key"},
            {"name": "Name", "type": "nvarchar(250)", "description": "Company name"},
            {"name": "TypeId", "type": "uniqueidentifier", "description": "FK to AccountType lookup"},
            {"name": "IndustryId", "type": "uniqueidentifier", "description": "FK to AccountIndustry lookup"},
            {"name": "OwnerId", "type": "uniqueidentifier", "description": "FK to Contact - account owner"},
            {"name": "PrimaryContactId", "type": "uniqueidentifier", "description": "FK to Contact - primary contact"},
            {"name": "Phone", "type": "nvarchar(250)", "description": "Main phone number"},
            {"name": "Web", "type": "nvarchar(250)", "description": "Website URL"},
            {"name": "AnnualRevenue", "type": "decimal", "description": "Annual revenue amount"},
            {"name": "EmployeesNumber", "type": "int", "description": "Number of employees"},
            {"name": "CreatedOn", "type": "datetime", "description": "Record creation timestamp"},
            {"name": "ModifiedOn", "type": "datetime", "description": "Last modification timestamp"},
        ],
        "relationships": [
            {"entity": "Contact", "type": "one-to-many", "column": "AccountId"},
            {"entity": "Opportunity", "type": "one-to-many", "column": "AccountId"},
            {"entity": "Activity", "type": "one-to-many", "detail": True},
            {"entity": "Case", "type": "one-to-many", "column": "AccountId"},
        ]
    },
    "Opportunity": {
        "description": "Sales opportunity/deal tracking entity",
        "table_name": "Opportunity",
        "key_columns": [
            {"name": "Id", "type": "uniqueidentifier", "description": "Primary key"},
            {"name": "Title", "type": "nvarchar(250)", "description": "Opportunity name/title"},
            {"name": "AccountId", "type": "uniqueidentifier", "description": "FK to Account"},
            {"name": "StageId", "type": "uniqueidentifier", "description": "FK to OpportunityStage lookup"},
            {"name": "Amount", "type": "decimal", "description": "Deal value/amount"},
            {"name": "Probability", "type": "int", "description": "Win probability percentage"},
            {"name": "OwnerId", "type": "uniqueidentifier", "description": "FK to Contact - opportunity owner"},
            {"name": "CloseDate", "type": "datetime", "description": "Expected close date"},
            {"name": "DueDate", "type": "datetime", "description": "Due date"},
            {"name": "LeadTypeId", "type": "uniqueidentifier", "description": "FK to LeadType - source type"},
            {"name": "IsPrimary", "type": "bit", "description": "Primary opportunity flag"},
            {"name": "CreatedOn", "type": "datetime", "description": "Record creation timestamp"},
            {"name": "ModifiedOn", "type": "datetime", "description": "Last modification timestamp"},
        ],
        "relationships": [
            {"entity": "Account", "type": "many-to-one", "column": "AccountId"},
            {"entity": "Contact", "type": "many-to-many", "via": "OpportunityContact"},
            {"entity": "OpportunityStage", "type": "many-to-one", "column": "StageId"},
            {"entity": "Product", "type": "many-to-many", "via": "OpportunityProductInterest"},
            {"entity": "Activity", "type": "one-to-many", "detail": True},
        ]
    },
    "Lead": {
        "description": "Sales lead entity - potential customers before qualification",
        "table_name": "Lead",
        "key_columns": [
            {"name": "Id", "type": "uniqueidentifier", "description": "Primary key"},
            {"name": "LeadName", "type": "nvarchar(250)", "description": "Lead name/title"},
            {"name": "Contact", "type": "nvarchar(250)", "description": "Contact person name"},
            {"name": "Account", "type": "nvarchar(250)", "description": "Company name (text)"},
            {"name": "Email", "type": "nvarchar(250)", "description": "Email address"},
            {"name": "MobilePhone", "type": "nvarchar(250)", "description": "Mobile phone"},
            {"name": "QualifyStatusId", "type": "uniqueidentifier", "description": "FK to QualifyStatus lookup"},
            {"name": "LeadSourceId", "type": "uniqueidentifier", "description": "FK to LeadSource lookup"},
            {"name": "LeadTypeId", "type": "uniqueidentifier", "description": "FK to LeadType lookup"},
            {"name": "OwnerId", "type": "uniqueidentifier", "description": "FK to Contact - lead owner"},
            {"name": "QualifiedContactId", "type": "uniqueidentifier", "description": "FK to Contact - converted contact"},
            {"name": "QualifiedAccountId", "type": "uniqueidentifier", "description": "FK to Account - converted account"},
            {"name": "Budget", "type": "decimal", "description": "Estimated budget"},
            {"name": "CreatedOn", "type": "datetime", "description": "Record creation timestamp"},
        ],
        "relationships": [
            {"entity": "Contact", "type": "one-to-one", "column": "QualifiedContactId"},
            {"entity": "Account", "type": "one-to-one", "column": "QualifiedAccountId"},
            {"entity": "Activity", "type": "one-to-many", "detail": True},
        ]
    },
    "Activity": {
        "description": "Activities including calls, emails, tasks, meetings",
        "table_name": "Activity",
        "key_columns": [
            {"name": "Id", "type": "uniqueidentifier", "description": "Primary key"},
            {"name": "Title", "type": "nvarchar(500)", "description": "Activity subject/title"},
            {"name": "TypeId", "type": "uniqueidentifier", "description": "FK to ActivityType lookup"},
            {"name": "StatusId", "type": "uniqueidentifier", "description": "FK to ActivityStatus lookup"},
            {"name": "PriorityId", "type": "uniqueidentifier", "description": "FK to ActivityPriority lookup"},
            {"name": "OwnerId", "type": "uniqueidentifier", "description": "FK to Contact - activity owner"},
            {"name": "ContactId", "type": "uniqueidentifier", "description": "FK to Contact - related contact"},
            {"name": "AccountId", "type": "uniqueidentifier", "description": "FK to Account - related account"},
            {"name": "OpportunityId", "type": "uniqueidentifier", "description": "FK to Opportunity"},
            {"name": "StartDate", "type": "datetime", "description": "Activity start date/time"},
            {"name": "DueDate", "type": "datetime", "description": "Activity due date/time"},
            {"name": "ResultId", "type": "uniqueidentifier", "description": "FK to ActivityResult lookup"},
            {"name": "CreatedOn", "type": "datetime", "description": "Record creation timestamp"},
        ],
        "relationships": [
            {"entity": "Contact", "type": "many-to-one", "column": "ContactId"},
            {"entity": "Account", "type": "many-to-one", "column": "AccountId"},
            {"entity": "Opportunity", "type": "many-to-one", "column": "OpportunityId"},
            {"entity": "ActivityParticipant", "type": "one-to-many", "detail": True},
        ]
    },
    "Case": {
        "description": "Customer service case/ticket entity",
        "table_name": "Case",
        "key_columns": [
            {"name": "Id", "type": "uniqueidentifier", "description": "Primary key"},
            {"name": "Number", "type": "nvarchar(250)", "description": "Case number"},
            {"name": "Subject", "type": "nvarchar(500)", "description": "Case subject"},
            {"name": "StatusId", "type": "uniqueidentifier", "description": "FK to CaseStatus lookup"},
            {"name": "PriorityId", "type": "uniqueidentifier", "description": "FK to CasePriority lookup"},
            {"name": "CategoryId", "type": "uniqueidentifier", "description": "FK to CaseCategory lookup"},
            {"name": "ContactId", "type": "uniqueidentifier", "description": "FK to Contact - reporting contact"},
            {"name": "AccountId", "type": "uniqueidentifier", "description": "FK to Account - associated account"},
            {"name": "OwnerId", "type": "uniqueidentifier", "description": "FK to Contact - case owner"},
            {"name": "GroupId", "type": "uniqueidentifier", "description": "FK to SysAdminUnit - assigned group"},
            {"name": "RegisteredOn", "type": "datetime", "description": "Registration timestamp"},
            {"name": "SolutionDate", "type": "datetime", "description": "Solution/resolution date"},
            {"name": "SatisfactionLevelId", "type": "uniqueidentifier", "description": "FK to SatisfactionLevel lookup"},
            {"name": "CreatedOn", "type": "datetime", "description": "Record creation timestamp"},
        ],
        "relationships": [
            {"entity": "Contact", "type": "many-to-one", "column": "ContactId"},
            {"entity": "Account", "type": "many-to-one", "column": "AccountId"},
            {"entity": "Activity", "type": "one-to-many", "detail": True},
        ]
    },
    "Product": {
        "description": "Product catalog entity",
        "table_name": "Product",
        "key_columns": [
            {"name": "Id", "type": "uniqueidentifier", "description": "Primary key"},
            {"name": "Name", "type": "nvarchar(250)", "description": "Product name"},
            {"name": "Code", "type": "nvarchar(50)", "description": "Product code/SKU"},
            {"name": "TypeId", "type": "uniqueidentifier", "description": "FK to ProductType lookup"},
            {"name": "CategoryId", "type": "uniqueidentifier", "description": "FK to ProductCategory lookup"},
            {"name": "Price", "type": "decimal", "description": "Unit price"},
            {"name": "IsActive", "type": "bit", "description": "Active flag"},
            {"name": "Description", "type": "nvarchar(max)", "description": "Product description"},
            {"name": "CreatedOn", "type": "datetime", "description": "Record creation timestamp"},
        ],
        "relationships": [
            {"entity": "Opportunity", "type": "many-to-many", "via": "OpportunityProductInterest"},
            {"entity": "Order", "type": "one-to-many", "via": "OrderProduct"},
        ]
    },
    "Order": {
        "description": "Sales order entity",
        "table_name": "Order",
        "key_columns": [
            {"name": "Id", "type": "uniqueidentifier", "description": "Primary key"},
            {"name": "Number", "type": "nvarchar(250)", "description": "Order number"},
            {"name": "AccountId", "type": "uniqueidentifier", "description": "FK to Account - customer"},
            {"name": "ContactId", "type": "uniqueidentifier", "description": "FK to Contact - order contact"},
            {"name": "OpportunityId", "type": "uniqueidentifier", "description": "FK to Opportunity - source opportunity"},
            {"name": "StatusId", "type": "uniqueidentifier", "description": "FK to OrderStatus lookup"},
            {"name": "Amount", "type": "decimal", "description": "Order total amount"},
            {"name": "OwnerId", "type": "uniqueidentifier", "description": "FK to Contact - order owner"},
            {"name": "Date", "type": "datetime", "description": "Order date"},
            {"name": "CreatedOn", "type": "datetime", "description": "Record creation timestamp"},
        ],
        "relationships": [
            {"entity": "Account", "type": "many-to-one", "column": "AccountId"},
            {"entity": "Contact", "type": "many-to-one", "column": "ContactId"},
            {"entity": "Opportunity", "type": "many-to-one", "column": "OpportunityId"},
            {"entity": "OrderProduct", "type": "one-to-many", "detail": True},
        ]
    },
    "SysAdminUnit": {
        "description": "System users and groups (security model)",
        "table_name": "SysAdminUnit",
        "key_columns": [
            {"name": "Id", "type": "uniqueidentifier", "description": "Primary key"},
            {"name": "Name", "type": "nvarchar(250)", "description": "User/group name"},
            {"name": "ContactId", "type": "uniqueidentifier", "description": "FK to Contact - linked contact"},
            {"name": "SysAdminUnitTypeId", "type": "uniqueidentifier", "description": "FK - user type (user, role, org)"},
            {"name": "ParentRoleId", "type": "uniqueidentifier", "description": "FK to parent role/group"},
            {"name": "Active", "type": "bit", "description": "Active flag"},
            {"name": "LoggedIn", "type": "bit", "description": "Currently logged in flag"},
        ],
        "relationships": [
            {"entity": "Contact", "type": "one-to-one", "column": "ContactId"},
            {"entity": "SysAdminUnit", "type": "self-referencing", "column": "ParentRoleId"},
        ]
    },
}


class SchemaExplorerInput(BaseModel):
    """Input schema for schema exploration."""
    entity_name: str = Field(description="Name of the Creatio entity to explore (e.g., Contact, Account, Opportunity)")
    include_relationships: bool = Field(default=True, description="Whether to include relationship information")


class EntityRelationshipInput(BaseModel):
    """Input schema for entity relationship analysis."""
    source_entity: str = Field(description="Source entity name")
    target_entity: Optional[str] = Field(default=None, description="Target entity (optional - shows all if not specified)")
    relationship_depth: int = Field(default=2, description="How many levels of relationships to explore")


class ColumnAnalyzerInput(BaseModel):
    """Input schema for column analysis."""
    entity_name: str = Field(description="Entity name to analyze columns for")
    column_filter: Optional[str] = Field(default=None, description="Filter columns by name pattern")
    include_system_columns: bool = Field(default=False, description="Include system columns like CreatedOn, ModifiedOn")


class SchemaSearchInput(BaseModel):
    """Input schema for schema search."""
    search_term: str = Field(description="Term to search for in entity names, column names, or descriptions")
    search_scope: str = Field(default="all", description="Where to search: all, entities, columns, relationships")


class SchemaExplorerTool(BaseTool):
    """Tool for exploring Creatio CRM schema."""
    
    name: str = "schema_explorer"
    description: str = (
        "Explores the Creatio CRM database schema for a specific entity. "
        "Returns detailed information about tables, columns, data types, "
        "and relationships. Use this to understand how data is structured."
    )
    args_schema: Type[BaseModel] = SchemaExplorerInput
    
    def _run(self, entity_name: str, include_relationships: bool = True) -> str:
        """Explore schema for an entity."""
        entity_key = entity_name.strip()
        
        # Try case-insensitive match
        matched_entity = None
        for key in CREATIO_SCHEMA_KNOWLEDGE:
            if key.lower() == entity_key.lower():
                matched_entity = key
                break
        
        if not matched_entity:
            available = list(CREATIO_SCHEMA_KNOWLEDGE.keys())
            return str({
                "success": False,
                "error": f"Entity '{entity_name}' not found in schema knowledge base",
                "available_entities": available,
                "suggestion": f"Try one of: {', '.join(available)}"
            })
        
        entity_info = CREATIO_SCHEMA_KNOWLEDGE[matched_entity]
        
        result = {
            "success": True,
            "entity": matched_entity,
            "table_name": entity_info["table_name"],
            "description": entity_info["description"],
            "columns": entity_info["key_columns"],
            "column_count": len(entity_info["key_columns"]),
        }
        
        if include_relationships:
            result["relationships"] = entity_info.get("relationships", [])
            result["relationship_count"] = len(entity_info.get("relationships", []))
        
        return str(result)


class EntityRelationshipTool(BaseTool):
    """Tool for analyzing entity relationships in Creatio CRM."""
    
    name: str = "entity_relationship_analyzer"
    description: str = (
        "Analyzes relationships between Creatio CRM entities. "
        "Shows how tables are connected through foreign keys, "
        "junction tables, and detail relationships."
    )
    args_schema: Type[BaseModel] = EntityRelationshipInput
    
    def _run(
        self, 
        source_entity: str, 
        target_entity: Optional[str] = None,
        relationship_depth: int = 2
    ) -> str:
        """Analyze entity relationships."""
        source_key = None
        for key in CREATIO_SCHEMA_KNOWLEDGE:
            if key.lower() == source_entity.lower():
                source_key = key
                break
        
        if not source_key:
            return str({
                "success": False,
                "error": f"Source entity '{source_entity}' not found",
                "available_entities": list(CREATIO_SCHEMA_KNOWLEDGE.keys())
            })
        
        source_info = CREATIO_SCHEMA_KNOWLEDGE[source_key]
        relationships = source_info.get("relationships", [])
        
        if target_entity:
            # Filter to specific target
            target_key = None
            for key in CREATIO_SCHEMA_KNOWLEDGE:
                if key.lower() == target_entity.lower():
                    target_key = key
                    break
            
            if target_key:
                relationships = [r for r in relationships if r["entity"].lower() == target_key.lower()]
        
        # Build relationship map
        result = {
            "success": True,
            "source_entity": source_key,
            "direct_relationships": relationships,
            "relationship_paths": []
        }
        
        # Find paths through relationships
        if relationship_depth > 1:
            for rel in relationships:
                related_entity = rel["entity"]
                if related_entity in CREATIO_SCHEMA_KNOWLEDGE:
                    secondary_rels = CREATIO_SCHEMA_KNOWLEDGE[related_entity].get("relationships", [])
                    for sec_rel in secondary_rels[:3]:  # Limit secondary relationships
                        if sec_rel["entity"] != source_key:
                            result["relationship_paths"].append({
                                "path": f"{source_key} -> {related_entity} -> {sec_rel['entity']}",
                                "via_relationship": rel["type"],
                                "secondary_relationship": sec_rel["type"]
                            })
        
        return str(result)


class ColumnAnalyzerTool(BaseTool):
    """Tool for detailed column analysis."""
    
    name: str = "column_analyzer"
    description: str = (
        "Provides detailed analysis of columns in a Creatio CRM entity. "
        "Shows column types, purposes, constraints, and usage recommendations."
    )
    args_schema: Type[BaseModel] = ColumnAnalyzerInput
    
    def _run(
        self,
        entity_name: str,
        column_filter: Optional[str] = None,
        include_system_columns: bool = False
    ) -> str:
        """Analyze columns for an entity."""
        entity_key = None
        for key in CREATIO_SCHEMA_KNOWLEDGE:
            if key.lower() == entity_name.lower():
                entity_key = key
                break
        
        if not entity_key:
            return str({
                "success": False,
                "error": f"Entity '{entity_name}' not found"
            })
        
        columns = CREATIO_SCHEMA_KNOWLEDGE[entity_key]["key_columns"]
        
        # System column patterns
        system_columns = ["CreatedOn", "ModifiedOn", "CreatedById", "ModifiedById", "ProcessListeners"]
        
        if not include_system_columns:
            columns = [c for c in columns if c["name"] not in system_columns]
        
        if column_filter:
            columns = [c for c in columns if column_filter.lower() in c["name"].lower()]
        
        # Categorize columns
        categorized = {
            "primary_key": [],
            "foreign_keys": [],
            "lookup_references": [],
            "data_columns": [],
            "datetime_columns": [],
        }
        
        for col in columns:
            if col["name"] == "Id":
                categorized["primary_key"].append(col)
            elif col["name"].endswith("Id") and col["type"] == "uniqueidentifier":
                if "FK" in col["description"]:
                    categorized["foreign_keys"].append(col)
                else:
                    categorized["lookup_references"].append(col)
            elif "datetime" in col["type"]:
                categorized["datetime_columns"].append(col)
            else:
                categorized["data_columns"].append(col)
        
        result = {
            "success": True,
            "entity": entity_key,
            "total_columns": len(columns),
            "columns": columns,
            "categorized": categorized,
            "analysis": {
                "has_primary_key": len(categorized["primary_key"]) > 0,
                "foreign_key_count": len(categorized["foreign_keys"]),
                "is_highly_relational": len(categorized["foreign_keys"]) > 3,
            }
        }
        
        return str(result)


class SchemaSearchTool(BaseTool):
    """Tool for searching across the Creatio schema."""
    
    name: str = "schema_search"
    description: str = (
        "Searches across the Creatio CRM schema for entities, columns, "
        "or relationships matching a search term. Use to find relevant "
        "tables or columns when you know part of the name or concept."
    )
    args_schema: Type[BaseModel] = SchemaSearchInput
    
    def _run(self, search_term: str, search_scope: str = "all") -> str:
        """Search the schema."""
        term = search_term.lower()
        results = {
            "success": True,
            "search_term": search_term,
            "scope": search_scope,
            "matches": {
                "entities": [],
                "columns": [],
                "relationships": []
            }
        }
        
        for entity_name, entity_info in CREATIO_SCHEMA_KNOWLEDGE.items():
            # Search entities
            if search_scope in ["all", "entities"]:
                if term in entity_name.lower() or term in entity_info["description"].lower():
                    results["matches"]["entities"].append({
                        "entity": entity_name,
                        "description": entity_info["description"],
                        "table": entity_info["table_name"]
                    })
            
            # Search columns
            if search_scope in ["all", "columns"]:
                for col in entity_info["key_columns"]:
                    if term in col["name"].lower() or term in col["description"].lower():
                        results["matches"]["columns"].append({
                            "entity": entity_name,
                            "column": col["name"],
                            "type": col["type"],
                            "description": col["description"]
                        })
            
            # Search relationships
            if search_scope in ["all", "relationships"]:
                for rel in entity_info.get("relationships", []):
                    if term in rel["entity"].lower() or term in rel["type"].lower():
                        results["matches"]["relationships"].append({
                            "from_entity": entity_name,
                            "to_entity": rel["entity"],
                            "type": rel["type"]
                        })
        
        # Add summary
        results["summary"] = {
            "total_matches": (
                len(results["matches"]["entities"]) +
                len(results["matches"]["columns"]) +
                len(results["matches"]["relationships"])
            ),
            "entities_found": len(results["matches"]["entities"]),
            "columns_found": len(results["matches"]["columns"]),
            "relationships_found": len(results["matches"]["relationships"])
        }
        
        return str(results)
