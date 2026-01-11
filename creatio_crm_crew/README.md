# Creatio CRM Backend Analysis Crew

AI-powered agent system for analyzing and understanding the Creatio CRM backend. This crew helps data architects and staff understand the schema, structure, and extract meaningful metrics and KPIs from the system.

## Overview

The Creatio CRM Backend Analysis Crew consists of four specialized AI agents:

1. **Schema Analyst** - Explores and explains database schema, tables, columns, and relationships
2. **Data Architect** - Provides architectural guidance and data modeling recommendations
3. **Metrics Expert** - Helps define and calculate KPIs and metrics for business insights
4. **Query Builder** - Constructs efficient SQL and OData queries for data extraction

## Installation

```bash
# Install dependencies
pip install -e .

# Or with dev dependencies
pip install -e ".[dev]"
```

## Configuration

Copy the example environment file and configure your settings:

```bash
cp creatio_crm_crew.env.example .env
```

At minimum, you need to set your OpenAI API key:

```
OPENAI_API_KEY=sk-your-key-here
```

## Quick Start

### Using Python

```python
from creatio_crm_crew import CreatioCRMCrew

# Initialize the crew
crew = CreatioCRMCrew(verbose=True)

# Ask any question about Creatio CRM
result = crew.ask_question("What tables store customer information?")
print(result)

# Explore a specific entity
result = crew.explore_entity("Contact")
print(result)

# Build a query from a business question
result = crew.build_query("Show me all opportunities over $10,000 closing this month")
print(result)

# Define KPIs for a business goal
result = crew.define_kpis("Improve sales performance", context="B2B software company")
print(result)
```

### Using CLI

```bash
# Ask a question
creatio-crm ask "What are the key fields in the Contact entity?"

# Explore an entity
creatio-crm schema explore Contact

# Build a query
creatio-crm query build "Show me open opportunities by account"

# Design a dashboard
creatio-crm metrics dashboard "Sales Performance" --audience manager

# Generate documentation
creatio-crm docs generate --entities "Contact,Account,Opportunity"

# Start interactive mode
creatio-crm interactive
```

## Features

### Schema Exploration

- Explore any Creatio entity's structure
- Understand relationships between entities
- Search across the schema
- Get a complete schema overview

```python
# Explore an entity
crew.explore_entity("Opportunity")

# Analyze relationships
crew.analyze_relationships("Contact", "Account")

# Get schema overview
crew.get_schema_overview()
```

### Query Building

- Translate business questions to SQL queries
- Build OData queries for the Creatio API
- Optimize existing queries
- Create reusable query templates

```python
# Build from business question
crew.build_query("List all contacts with their account names")

# Build report query
crew.build_report_query(
    report_description="Sales by industry",
    entities="Opportunity, Account",
    time_range="this quarter"
)

# Build OData query
crew.build_odata_query(
    entity="Contact",
    requirements="Get active contacts with account info"
)

# Optimize a query
crew.optimize_query(your_sql_query)
```

### Metrics & KPIs

- Define KPIs for business goals
- Calculate specific metrics
- Get role-based metric recommendations
- Design dashboards
- Analyze sales pipeline

```python
# Define KPIs
crew.define_kpis("Improve customer retention")

# Calculate metric
crew.calculate_metric("sales.win_rate", time_period="last_quarter")

# Recommend metrics for a role
crew.recommend_metrics(role="manager", focus_area="sales")

# Design dashboard
crew.design_dashboard(purpose="Executive Overview", audience="executive")

# Analyze pipeline
crew.analyze_sales_pipeline(depth="deep")
```

### Documentation Generation

- Generate entity documentation
- Create data dictionaries
- Generate ERDs (Mermaid, PlantUML, DBML)
- Create integration guides

```python
# Generate documentation
crew.generate_documentation(entities="Contact, Account")

# Create data dictionary
crew.create_data_dictionary("Opportunity")

# Generate ERD
crew.generate_erd(entities="Contact, Account, Opportunity", include_columns=True)

# Create integration guide
crew.create_integration_guide(
    source_system="Salesforce",
    target_entities="Contact, Account"
)
```

## Supported Creatio Entities

The crew has built-in knowledge of common Creatio CRM entities:

- **Contact** - Individual/person records
- **Account** - Company/organization records
- **Opportunity** - Sales deals/opportunities
- **Lead** - Sales leads
- **Activity** - Calls, emails, meetings, tasks
- **Case** - Customer service cases
- **Product** - Product catalog
- **Order** - Sales orders
- **SysAdminUnit** - System users and groups

## Available KPIs

The metrics expert has knowledge of standard CRM KPIs:

### Sales
- Pipeline Value
- Win Rate
- Average Deal Size
- Sales Cycle Length
- Revenue by Rep
- Lead Conversion Rate

### Marketing
- Lead Volume
- Lead Source Effectiveness
- Marketing Qualified Leads
- Cost per Lead

### Customer Service
- Case Volume
- Resolution Time
- First Response Time
- Customer Satisfaction (CSAT)
- SLA Compliance

### Customer Health
- Customer Lifetime Value
- Churn Rate
- Net Promoter Score
- Revenue Retention

## CLI Commands

```bash
# Schema commands
creatio-crm schema explore <entity>
creatio-crm schema relationships <source> [--target <target>]
creatio-crm schema overview
creatio-crm schema ask "<question>"

# Query commands
creatio-crm query build "<question>"
creatio-crm query report "<description>" --entities "<entities>"
creatio-crm query odata <entity> --requirements "<requirements>"
creatio-crm query optimize "<query>" [--type sql|odata]

# Metrics commands
creatio-crm metrics define "<goal>" [--context "<context>"]
creatio-crm metrics calculate <metric> [--period <period>]
creatio-crm metrics recommend --role <role> --focus "<area>"
creatio-crm metrics dashboard "<purpose>" [--audience <audience>]
creatio-crm metrics pipeline [--depth quick|standard|deep]

# Documentation commands
creatio-crm docs generate [--entities "<entities>"]
creatio-crm docs dictionary <entity>
creatio-crm docs erd [--entities "<entities>"] [--columns|--no-columns]
creatio-crm docs integration <source_system> --entities "<entities>"

# General commands
creatio-crm ask "<question>"
creatio-crm analyze <entity>
creatio-crm interactive
```

## Architecture

```
creatio_crm_crew/
├── __init__.py          # Package initialization
├── crew.py              # Main CreatioCRMCrew orchestration
├── cli.py               # Command-line interface
├── main.py              # Entry point
├── config/
│   └── settings.py      # Configuration management
├── agents/
│   ├── schema_analyst_agent.py
│   ├── data_architect_agent.py
│   ├── metrics_expert_agent.py
│   └── query_builder_agent.py
├── tasks/
│   ├── schema_tasks.py
│   ├── query_tasks.py
│   ├── metrics_tasks.py
│   └── documentation_tasks.py
└── tools/
    ├── schema_tools.py      # Schema exploration tools
    ├── query_tools.py       # Query building tools
    ├── metrics_tools.py     # KPI and metrics tools
    └── documentation_tools.py # Doc generation tools
```

## Extending the Crew

### Adding New Entities

Edit `creatio_crm_crew/tools/schema_tools.py` and add to the `CREATIO_SCHEMA_KNOWLEDGE` dictionary:

```python
CREATIO_SCHEMA_KNOWLEDGE["YourEntity"] = {
    "description": "Description of the entity",
    "table_name": "YourEntity",
    "key_columns": [
        {"name": "Id", "type": "uniqueidentifier", "description": "Primary key"},
        # Add more columns...
    ],
    "relationships": [
        {"entity": "RelatedEntity", "type": "many-to-one", "column": "RelatedEntityId"},
    ]
}
```

### Adding New KPIs

Edit `creatio_crm_crew/tools/metrics_tools.py` and add to the `CRM_KPI_LIBRARY`:

```python
CRM_KPI_LIBRARY["your_category"]["your_kpi"] = {
    "name": "Your KPI Name",
    "description": "Description of what it measures",
    "formula": "SUM(Amount) / COUNT(*)",
    "unit": "currency",  # or percentage, count, days, etc.
    "frequency": "monthly",
    "entities": ["Entity1", "Entity2"]
}
```

## Requirements

- Python 3.10+
- CrewAI 0.86.0+
- OpenAI API key (or Anthropic)

## License

MIT
