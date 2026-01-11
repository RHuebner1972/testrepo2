"""
Documentation generation tools for Creatio CRM schema and data.
"""

from typing import Type, Optional, List
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

from creatio_crm_crew.tools.schema_tools import CREATIO_SCHEMA_KNOWLEDGE


class SchemaDocInput(BaseModel):
    """Input schema for schema documentation generation."""
    entities: str = Field(description="Comma-separated list of entities to document (or 'all')")
    format: str = Field(default="markdown", description="Output format: markdown, html, json")
    include_relationships: bool = Field(default=True, description="Include relationship documentation")
    include_examples: bool = Field(default=True, description="Include example queries")


class DataDictionaryInput(BaseModel):
    """Input schema for data dictionary generation."""
    entity: str = Field(description="Entity to create data dictionary for")
    include_lookup_values: bool = Field(default=False, description="Include lookup/reference value samples")


class ERDInput(BaseModel):
    """Input schema for ERD generation."""
    entities: str = Field(description="Comma-separated list of entities to include (or 'all')")
    format: str = Field(default="mermaid", description="Output format: mermaid, plantuml, dbml")
    show_columns: bool = Field(default=False, description="Include column details in diagram")


class SchemaDocGeneratorTool(BaseTool):
    """Tool for generating schema documentation."""
    
    name: str = "schema_doc_generator"
    description: str = (
        "Generates comprehensive documentation for Creatio CRM schema. "
        "Creates human-readable documentation including entity descriptions, "
        "column details, and relationships."
    )
    args_schema: Type[BaseModel] = SchemaDocInput
    
    def _run(
        self,
        entities: str,
        format: str = "markdown",
        include_relationships: bool = True,
        include_examples: bool = True
    ) -> str:
        """Generate schema documentation."""
        # Parse entity list
        if entities.lower() == "all":
            entity_list = list(CREATIO_SCHEMA_KNOWLEDGE.keys())
        else:
            entity_list = [e.strip() for e in entities.split(",")]
        
        # Validate entities
        valid_entities = []
        for entity in entity_list:
            for key in CREATIO_SCHEMA_KNOWLEDGE:
                if key.lower() == entity.lower():
                    valid_entities.append(key)
                    break
        
        if not valid_entities:
            return str({
                "success": False,
                "error": "No valid entities found",
                "available_entities": list(CREATIO_SCHEMA_KNOWLEDGE.keys())
            })
        
        # Generate documentation based on format
        if format.lower() == "markdown":
            doc = self._generate_markdown(valid_entities, include_relationships, include_examples)
        elif format.lower() == "json":
            doc = self._generate_json(valid_entities, include_relationships)
        else:
            doc = self._generate_markdown(valid_entities, include_relationships, include_examples)
        
        result = {
            "success": True,
            "entities_documented": valid_entities,
            "format": format,
            "documentation": doc,
            "metadata": {
                "entity_count": len(valid_entities),
                "total_columns": sum(len(CREATIO_SCHEMA_KNOWLEDGE[e]["key_columns"]) for e in valid_entities),
                "total_relationships": sum(len(CREATIO_SCHEMA_KNOWLEDGE[e].get("relationships", [])) for e in valid_entities)
            }
        }
        
        return str(result)
    
    def _generate_markdown(self, entities: List[str], include_rels: bool, include_examples: bool) -> str:
        """Generate Markdown documentation."""
        doc = "# Creatio CRM Schema Documentation\n\n"
        doc += f"*Documentation for {len(entities)} entities*\n\n"
        doc += "---\n\n"
        
        for entity in entities:
            info = CREATIO_SCHEMA_KNOWLEDGE[entity]
            
            doc += f"## {entity}\n\n"
            doc += f"**Description:** {info['description']}\n\n"
            doc += f"**Table Name:** `{info['table_name']}`\n\n"
            
            # Columns table
            doc += "### Columns\n\n"
            doc += "| Column | Type | Description |\n"
            doc += "|--------|------|-------------|\n"
            
            for col in info["key_columns"]:
                doc += f"| {col['name']} | {col['type']} | {col['description']} |\n"
            
            doc += "\n"
            
            # Relationships
            if include_rels and info.get("relationships"):
                doc += "### Relationships\n\n"
                for rel in info["relationships"]:
                    rel_type = rel["type"]
                    target = rel["entity"]
                    via = rel.get("column", rel.get("via", ""))
                    doc += f"- **{target}** ({rel_type})"
                    if via:
                        doc += f" via `{via}`"
                    doc += "\n"
                doc += "\n"
            
            # Example queries
            if include_examples:
                doc += "### Example Queries\n\n"
                doc += "```sql\n"
                doc += f"-- Get all {entity} records\n"
                doc += f"SELECT TOP 100 * FROM [{info['table_name']}]\n\n"
                doc += f"-- Get {entity} with specific columns\n"
                cols = [c["name"] for c in info["key_columns"][:5]]
                doc += f"SELECT {', '.join(cols)} FROM [{info['table_name']}]\n"
                doc += "```\n\n"
            
            doc += "---\n\n"
        
        return doc
    
    def _generate_json(self, entities: List[str], include_rels: bool) -> dict:
        """Generate JSON documentation."""
        doc = {"entities": {}}
        
        for entity in entities:
            info = CREATIO_SCHEMA_KNOWLEDGE[entity]
            
            entity_doc = {
                "name": entity,
                "table_name": info["table_name"],
                "description": info["description"],
                "columns": info["key_columns"]
            }
            
            if include_rels:
                entity_doc["relationships"] = info.get("relationships", [])
            
            doc["entities"][entity] = entity_doc
        
        return doc


class DataDictionaryTool(BaseTool):
    """Tool for generating data dictionaries."""
    
    name: str = "data_dictionary"
    description: str = (
        "Creates a detailed data dictionary for Creatio CRM entities. "
        "Includes column specifications, data types, constraints, "
        "and business definitions."
    )
    args_schema: Type[BaseModel] = DataDictionaryInput
    
    def _run(
        self,
        entity: str,
        include_lookup_values: bool = False
    ) -> str:
        """Generate data dictionary."""
        # Find entity
        entity_key = None
        for key in CREATIO_SCHEMA_KNOWLEDGE:
            if key.lower() == entity.lower():
                entity_key = key
                break
        
        if not entity_key:
            return str({
                "success": False,
                "error": f"Entity '{entity}' not found",
                "available_entities": list(CREATIO_SCHEMA_KNOWLEDGE.keys())
            })
        
        info = CREATIO_SCHEMA_KNOWLEDGE[entity_key]
        
        # Build detailed data dictionary
        columns_detail = []
        for col in info["key_columns"]:
            col_detail = {
                "column_name": col["name"],
                "data_type": col["type"],
                "description": col["description"],
                "nullable": col["name"] != "Id",  # Assume Id is not nullable
                "is_primary_key": col["name"] == "Id",
                "is_foreign_key": col["name"].endswith("Id") and col["name"] != "Id",
                "business_rules": self._get_business_rules(col),
                "sample_values": self._get_sample_values(col, include_lookup_values)
            }
            
            if col_detail["is_foreign_key"]:
                col_detail["references"] = self._identify_reference(col)
            
            columns_detail.append(col_detail)
        
        dictionary = {
            "success": True,
            "entity": entity_key,
            "table_name": info["table_name"],
            "description": info["description"],
            "data_dictionary": {
                "columns": columns_detail,
                "column_count": len(columns_detail),
                "primary_key": "Id",
                "foreign_key_count": sum(1 for c in columns_detail if c["is_foreign_key"]),
                "indexes_recommended": self._recommend_indexes(columns_detail)
            },
            "audit_columns": {
                "CreatedOn": "Record creation timestamp",
                "ModifiedOn": "Last modification timestamp",
                "CreatedById": "User who created the record",
                "ModifiedById": "User who last modified the record"
            },
            "notes": [
                "All timestamps are stored in UTC",
                "GUID columns use uniqueidentifier type",
                "Lookup references point to Id columns in related tables"
            ]
        }
        
        return str(dictionary)
    
    def _get_business_rules(self, col: dict) -> List[str]:
        """Get business rules for a column."""
        rules = []
        
        if col["name"] == "Id":
            rules.append("Auto-generated GUID primary key")
        elif col["name"] == "Name":
            rules.append("Required field for record identification")
        elif col["name"] == "Email":
            rules.append("Must be valid email format")
            rules.append("Should be unique for Contact records")
        elif "Phone" in col["name"]:
            rules.append("Phone number format validation recommended")
        elif col["name"] == "OwnerId":
            rules.append("Must reference active system user")
            rules.append("Used for record ownership and security")
        elif "Date" in col["name"]:
            rules.append("Date validation - cannot be historical for future-dated fields")
        elif col["name"] == "Amount" or col["type"] == "decimal":
            rules.append("Non-negative value constraint recommended")
        
        return rules
    
    def _get_sample_values(self, col: dict, include_lookups: bool) -> List[str]:
        """Get sample values for a column."""
        if col["type"] == "uniqueidentifier":
            return ["00000000-0000-0000-0000-000000000001"]
        elif col["type"].startswith("nvarchar"):
            if "Email" in col["name"]:
                return ["john.doe@example.com", "jane.smith@company.org"]
            elif "Phone" in col["name"]:
                return ["+1-555-123-4567", "(555) 987-6543"]
            elif "Name" in col["name"]:
                return ["Acme Corporation", "John Doe"]
            else:
                return ["Sample text value"]
        elif col["type"] == "datetime":
            return ["2026-01-15T10:30:00Z"]
        elif col["type"] == "decimal":
            return ["10000.00", "25000.50"]
        elif col["type"] == "int":
            return ["100", "500"]
        elif col["type"] == "bit":
            return ["1 (true)", "0 (false)"]
        
        return []
    
    def _identify_reference(self, col: dict) -> dict:
        """Identify what a foreign key references."""
        col_name = col["name"]
        
        # Common patterns in Creatio
        references = {
            "AccountId": {"table": "Account", "column": "Id"},
            "ContactId": {"table": "Contact", "column": "Id"},
            "OwnerId": {"table": "Contact", "column": "Id"},
            "OpportunityId": {"table": "Opportunity", "column": "Id"},
            "LeadId": {"table": "Lead", "column": "Id"},
            "ActivityId": {"table": "Activity", "column": "Id"},
            "TypeId": {"table": f"{col_name.replace('Id', '')}Type", "column": "Id"},
            "StatusId": {"table": f"{col_name.replace('Id', '')}Status", "column": "Id"},
            "CategoryId": {"table": f"{col_name.replace('Id', '')}Category", "column": "Id"},
            "StageId": {"table": "OpportunityStage", "column": "Id"},
            "PriorityId": {"table": "Priority", "column": "Id"},
        }
        
        return references.get(col_name, {"table": "Unknown", "column": "Id"})
    
    def _recommend_indexes(self, columns: List[dict]) -> List[str]:
        """Recommend indexes based on columns."""
        indexes = []
        
        for col in columns:
            if col["is_foreign_key"]:
                indexes.append(f"IX_{col['column_name']}")
        
        # Common query patterns
        indexes.extend([
            "IX_CreatedOn (for date range queries)",
            "IX_OwnerId_CreatedOn (for user activity queries)"
        ])
        
        return indexes


class ERDGeneratorTool(BaseTool):
    """Tool for generating Entity-Relationship Diagrams."""
    
    name: str = "erd_generator"
    description: str = (
        "Generates Entity-Relationship Diagrams for Creatio CRM schema. "
        "Outputs in Mermaid, PlantUML, or DBML format for visualization."
    )
    args_schema: Type[BaseModel] = ERDInput
    
    def _run(
        self,
        entities: str,
        format: str = "mermaid",
        show_columns: bool = False
    ) -> str:
        """Generate ERD."""
        # Parse entity list
        if entities.lower() == "all":
            entity_list = list(CREATIO_SCHEMA_KNOWLEDGE.keys())
        else:
            entity_list = [e.strip() for e in entities.split(",")]
        
        # Validate entities
        valid_entities = []
        for entity in entity_list:
            for key in CREATIO_SCHEMA_KNOWLEDGE:
                if key.lower() == entity.lower():
                    valid_entities.append(key)
                    break
        
        if not valid_entities:
            return str({
                "success": False,
                "error": "No valid entities found",
                "available_entities": list(CREATIO_SCHEMA_KNOWLEDGE.keys())
            })
        
        # Generate diagram based on format
        if format.lower() == "mermaid":
            diagram = self._generate_mermaid(valid_entities, show_columns)
        elif format.lower() == "plantuml":
            diagram = self._generate_plantuml(valid_entities, show_columns)
        elif format.lower() == "dbml":
            diagram = self._generate_dbml(valid_entities)
        else:
            diagram = self._generate_mermaid(valid_entities, show_columns)
        
        result = {
            "success": True,
            "entities_included": valid_entities,
            "format": format,
            "diagram": diagram,
            "usage_instructions": self._get_usage_instructions(format)
        }
        
        return str(result)
    
    def _generate_mermaid(self, entities: List[str], show_columns: bool) -> str:
        """Generate Mermaid ERD."""
        lines = ["erDiagram"]
        
        # Add entities
        for entity in entities:
            info = CREATIO_SCHEMA_KNOWLEDGE[entity]
            
            if show_columns:
                lines.append(f"    {entity} {{")
                for col in info["key_columns"][:8]:  # Limit columns for readability
                    col_type = col["type"].replace("(", "_").replace(")", "").replace(",", "")
                    pk = "PK" if col["name"] == "Id" else ""
                    fk = "FK" if col["name"].endswith("Id") and col["name"] != "Id" else ""
                    marker = pk or fk
                    lines.append(f"        {col_type} {col['name']} {marker}")
                lines.append("    }")
            else:
                lines.append(f"    {entity}")
        
        # Add relationships
        added_rels = set()
        for entity in entities:
            info = CREATIO_SCHEMA_KNOWLEDGE[entity]
            
            for rel in info.get("relationships", []):
                target = rel["entity"]
                if target not in entities:
                    continue
                
                rel_key = tuple(sorted([entity, target]))
                if rel_key in added_rels:
                    continue
                added_rels.add(rel_key)
                
                rel_type = rel["type"]
                if rel_type == "one-to-many":
                    lines.append(f"    {entity} ||--o{{ {target} : has")
                elif rel_type == "many-to-one":
                    lines.append(f"    {entity} }}o--|| {target} : belongs_to")
                elif rel_type == "many-to-many":
                    lines.append(f"    {entity} }}o--o{{ {target} : relates")
                elif rel_type == "one-to-one":
                    lines.append(f"    {entity} ||--|| {target} : is")
        
        return "\n".join(lines)
    
    def _generate_plantuml(self, entities: List[str], show_columns: bool) -> str:
        """Generate PlantUML ERD."""
        lines = ["@startuml", "skinparam linetype ortho", ""]
        
        # Add entities
        for entity in entities:
            info = CREATIO_SCHEMA_KNOWLEDGE[entity]
            
            if show_columns:
                lines.append(f"entity {entity} {{")
                lines.append(f"    * Id : uniqueidentifier <<PK>>")
                for col in info["key_columns"][1:6]:  # Skip Id, limit columns
                    fk = " <<FK>>" if col["name"].endswith("Id") else ""
                    lines.append(f"    {col['name']} : {col['type']}{fk}")
                lines.append("}")
            else:
                lines.append(f"entity {entity}")
        
        lines.append("")
        
        # Add relationships
        added_rels = set()
        for entity in entities:
            info = CREATIO_SCHEMA_KNOWLEDGE[entity]
            
            for rel in info.get("relationships", []):
                target = rel["entity"]
                if target not in entities:
                    continue
                
                rel_key = tuple(sorted([entity, target]))
                if rel_key in added_rels:
                    continue
                added_rels.add(rel_key)
                
                rel_type = rel["type"]
                if rel_type == "one-to-many":
                    lines.append(f"{entity} ||--o{{ {target}")
                elif rel_type == "many-to-one":
                    lines.append(f"{entity} }}o--|| {target}")
                elif rel_type == "many-to-many":
                    lines.append(f"{entity} }}o--o{{ {target}")
                elif rel_type == "one-to-one":
                    lines.append(f"{entity} ||--|| {target}")
        
        lines.append("")
        lines.append("@enduml")
        
        return "\n".join(lines)
    
    def _generate_dbml(self, entities: List[str]) -> str:
        """Generate DBML."""
        lines = ["// Creatio CRM Schema - DBML Format", ""]
        
        for entity in entities:
            info = CREATIO_SCHEMA_KNOWLEDGE[entity]
            
            lines.append(f"Table {info['table_name']} {{")
            
            for col in info["key_columns"]:
                col_line = f"    {col['name']} {col['type']}"
                
                if col["name"] == "Id":
                    col_line += " [pk]"
                elif col["name"].endswith("Id"):
                    ref_table = self._guess_reference_table(col["name"])
                    col_line += f" [ref: > {ref_table}.Id]"
                
                col_line += f" // {col['description']}"
                lines.append(col_line)
            
            lines.append("}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _guess_reference_table(self, col_name: str) -> str:
        """Guess the reference table from column name."""
        # Remove 'Id' suffix
        base_name = col_name[:-2]
        
        # Common mappings
        mappings = {
            "Owner": "Contact",
            "Account": "Account",
            "Contact": "Contact",
            "Opportunity": "Opportunity",
            "Lead": "Lead",
            "Stage": "OpportunityStage",
            "Status": "Status",
            "Type": "Type",
            "Priority": "Priority",
            "Category": "Category"
        }
        
        return mappings.get(base_name, base_name)
    
    def _get_usage_instructions(self, format: str) -> str:
        """Get usage instructions for the diagram format."""
        instructions = {
            "mermaid": (
                "To render this Mermaid diagram:\n"
                "1. Use Mermaid Live Editor: https://mermaid.live\n"
                "2. Paste in GitHub/GitLab markdown with ```mermaid code block\n"
                "3. Use VS Code with Mermaid extension"
            ),
            "plantuml": (
                "To render this PlantUML diagram:\n"
                "1. Use PlantUML Online: http://www.plantuml.com/plantuml\n"
                "2. Use VS Code with PlantUML extension\n"
                "3. Install PlantUML locally with Java runtime"
            ),
            "dbml": (
                "To render this DBML diagram:\n"
                "1. Use dbdiagram.io: https://dbdiagram.io\n"
                "2. Use DBML CLI tool for programmatic rendering\n"
                "3. Export to various formats including SQL"
            )
        }
        
        return instructions.get(format.lower(), "Use appropriate visualization tool for the format")
