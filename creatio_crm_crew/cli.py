"""
Command-line interface for Creatio CRM Backend Analysis Crew.
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()


def get_crew(verbose: bool = True):
    """Lazy load crew to avoid import time overhead."""
    from creatio_crm_crew.crew import CreatioCRMCrew
    return CreatioCRMCrew(verbose=verbose)


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    Creatio CRM Backend Analysis Crew
    
    AI-powered agents to help understand Creatio CRM's database schema,
    build queries, define metrics, and generate documentation.
    """
    pass


# =============================================================================
# SCHEMA COMMANDS
# =============================================================================

@cli.group()
def schema():
    """Schema exploration and analysis commands."""
    pass


@schema.command("explore")
@click.argument("entity")
@click.option("--quiet", "-q", is_flag=True, help="Reduce verbosity")
def explore_entity(entity: str, quiet: bool):
    """Explore a specific Creatio CRM entity."""
    console.print(f"\n[bold blue]Exploring entity: {entity}[/bold blue]\n")
    
    crew = get_crew(verbose=not quiet)
    result = crew.explore_entity(entity)
    
    console.print(Panel(str(result), title=f"Entity: {entity}", border_style="green"))


@schema.command("relationships")
@click.argument("source")
@click.option("--target", "-t", default=None, help="Specific target entity")
@click.option("--quiet", "-q", is_flag=True, help="Reduce verbosity")
def analyze_relationships(source: str, target: str, quiet: bool):
    """Analyze relationships between entities."""
    target_text = f" and {target}" if target else ""
    console.print(f"\n[bold blue]Analyzing relationships: {source}{target_text}[/bold blue]\n")
    
    crew = get_crew(verbose=not quiet)
    result = crew.analyze_relationships(source, target)
    
    console.print(Panel(str(result), title="Relationship Analysis", border_style="green"))


@schema.command("overview")
@click.option("--quiet", "-q", is_flag=True, help="Reduce verbosity")
def schema_overview(quiet: bool):
    """Get a complete overview of the Creatio CRM schema."""
    console.print("\n[bold blue]Generating schema overview...[/bold blue]\n")
    
    crew = get_crew(verbose=not quiet)
    result = crew.get_schema_overview()
    
    console.print(Panel(str(result), title="Schema Overview", border_style="green"))


@schema.command("ask")
@click.argument("question")
@click.option("--quiet", "-q", is_flag=True, help="Reduce verbosity")
def ask_schema(question: str, quiet: bool):
    """Ask a question about the schema."""
    console.print(f"\n[bold blue]Question: {question}[/bold blue]\n")
    
    crew = get_crew(verbose=not quiet)
    result = crew.ask_schema_question(question)
    
    console.print(Panel(str(result), title="Answer", border_style="green"))


# =============================================================================
# QUERY COMMANDS
# =============================================================================

@cli.group()
def query():
    """Query building and optimization commands."""
    pass


@query.command("build")
@click.argument("question")
@click.option("--quiet", "-q", is_flag=True, help="Reduce verbosity")
def build_query(question: str, quiet: bool):
    """Build a query from a business question."""
    console.print(f"\n[bold blue]Building query for: {question}[/bold blue]\n")
    
    crew = get_crew(verbose=not quiet)
    result = crew.build_query(question)
    
    console.print(Panel(str(result), title="Query Result", border_style="green"))


@query.command("report")
@click.argument("description")
@click.option("--entities", "-e", required=True, help="Main entities")
@click.option("--time-range", "-t", default=None, help="Time range filter")
@click.option("--quiet", "-q", is_flag=True, help="Reduce verbosity")
def build_report(description: str, entities: str, time_range: str, quiet: bool):
    """Build a SQL query for a report."""
    console.print(f"\n[bold blue]Building report query: {description}[/bold blue]\n")
    
    crew = get_crew(verbose=not quiet)
    result = crew.build_report_query(description, entities, time_range)
    
    console.print(Panel(str(result), title="Report Query", border_style="green"))


@query.command("odata")
@click.argument("entity")
@click.option("--requirements", "-r", required=True, help="Data requirements")
@click.option("--quiet", "-q", is_flag=True, help="Reduce verbosity")
def build_odata(entity: str, requirements: str, quiet: bool):
    """Build an OData query for the Creatio API."""
    console.print(f"\n[bold blue]Building OData query for: {entity}[/bold blue]\n")
    
    crew = get_crew(verbose=not quiet)
    result = crew.build_odata_query(entity, requirements)
    
    console.print(Panel(str(result), title="OData Query", border_style="green"))


@query.command("optimize")
@click.argument("query_text")
@click.option("--type", "-t", "query_type", default="sql", help="Query type (sql/odata)")
@click.option("--quiet", "-q", is_flag=True, help="Reduce verbosity")
def optimize_query(query_text: str, query_type: str, quiet: bool):
    """Optimize an existing query."""
    console.print(f"\n[bold blue]Optimizing {query_type.upper()} query...[/bold blue]\n")
    
    crew = get_crew(verbose=not quiet)
    result = crew.optimize_query(query_text, query_type)
    
    console.print(Panel(str(result), title="Optimized Query", border_style="green"))


# =============================================================================
# METRICS COMMANDS
# =============================================================================

@cli.group()
def metrics():
    """Metrics and KPI commands."""
    pass


@metrics.command("define")
@click.argument("goal")
@click.option("--context", "-c", default="", help="Additional context")
@click.option("--quiet", "-q", is_flag=True, help="Reduce verbosity")
def define_kpis(goal: str, context: str, quiet: bool):
    """Define KPIs for a business goal."""
    console.print(f"\n[bold blue]Defining KPIs for: {goal}[/bold blue]\n")
    
    crew = get_crew(verbose=not quiet)
    result = crew.define_kpis(goal, context)
    
    console.print(Panel(str(result), title="KPI Definitions", border_style="green"))


@metrics.command("calculate")
@click.argument("metric")
@click.option("--period", "-p", default="last_month", help="Time period")
@click.option("--dimensions", "-d", default=None, help="Breakdown dimensions")
@click.option("--quiet", "-q", is_flag=True, help="Reduce verbosity")
def calculate_metric(metric: str, period: str, dimensions: str, quiet: bool):
    """Calculate a specific metric."""
    console.print(f"\n[bold blue]Calculating: {metric}[/bold blue]\n")
    
    crew = get_crew(verbose=not quiet)
    result = crew.calculate_metric(metric, period, dimensions)
    
    console.print(Panel(str(result), title="Metric Calculation", border_style="green"))


@metrics.command("recommend")
@click.option("--role", "-r", required=True, help="User role")
@click.option("--focus", "-f", required=True, help="Focus area")
@click.option("--quiet", "-q", is_flag=True, help="Reduce verbosity")
def recommend_metrics(role: str, focus: str, quiet: bool):
    """Recommend metrics for a specific role."""
    console.print(f"\n[bold blue]Recommending metrics for {role} - {focus}[/bold blue]\n")
    
    crew = get_crew(verbose=not quiet)
    result = crew.recommend_metrics(role, focus)
    
    console.print(Panel(str(result), title="Metric Recommendations", border_style="green"))


@metrics.command("dashboard")
@click.argument("purpose")
@click.option("--audience", "-a", default="manager", help="Target audience")
@click.option("--quiet", "-q", is_flag=True, help="Reduce verbosity")
def design_dashboard(purpose: str, audience: str, quiet: bool):
    """Design a metrics dashboard."""
    console.print(f"\n[bold blue]Designing dashboard: {purpose}[/bold blue]\n")
    
    crew = get_crew(verbose=not quiet)
    result = crew.design_dashboard(purpose, audience)
    
    console.print(Panel(str(result), title="Dashboard Design", border_style="green"))


@metrics.command("pipeline")
@click.option("--depth", "-d", default="standard", help="Analysis depth")
@click.option("--quiet", "-q", is_flag=True, help="Reduce verbosity")
def analyze_pipeline(depth: str, quiet: bool):
    """Analyze sales pipeline metrics."""
    console.print(f"\n[bold blue]Analyzing sales pipeline ({depth})...[/bold blue]\n")
    
    crew = get_crew(verbose=not quiet)
    result = crew.analyze_sales_pipeline(depth)
    
    console.print(Panel(str(result), title="Pipeline Analysis", border_style="green"))


# =============================================================================
# DOCUMENTATION COMMANDS
# =============================================================================

@cli.group()
def docs():
    """Documentation generation commands."""
    pass


@docs.command("generate")
@click.option("--entities", "-e", default="all", help="Entities to document")
@click.option("--quiet", "-q", is_flag=True, help="Reduce verbosity")
def generate_docs(entities: str, quiet: bool):
    """Generate documentation for Creatio entities."""
    console.print(f"\n[bold blue]Generating documentation for: {entities}[/bold blue]\n")
    
    crew = get_crew(verbose=not quiet)
    result = crew.generate_documentation(entities)
    
    console.print(Panel(str(result), title="Documentation", border_style="green"))


@docs.command("dictionary")
@click.argument("entity")
@click.option("--quiet", "-q", is_flag=True, help="Reduce verbosity")
def create_dictionary(entity: str, quiet: bool):
    """Create a data dictionary for an entity."""
    console.print(f"\n[bold blue]Creating data dictionary for: {entity}[/bold blue]\n")
    
    crew = get_crew(verbose=not quiet)
    result = crew.create_data_dictionary(entity)
    
    console.print(Panel(str(result), title="Data Dictionary", border_style="green"))


@docs.command("erd")
@click.option("--entities", "-e", default="all", help="Entities to include")
@click.option("--columns/--no-columns", default=True, help="Include columns")
@click.option("--quiet", "-q", is_flag=True, help="Reduce verbosity")
def generate_erd(entities: str, columns: bool, quiet: bool):
    """Generate an Entity-Relationship Diagram."""
    console.print(f"\n[bold blue]Generating ERD for: {entities}[/bold blue]\n")
    
    crew = get_crew(verbose=not quiet)
    result = crew.generate_erd(entities, columns)
    
    console.print(Panel(str(result), title="ERD", border_style="green"))


@docs.command("integration")
@click.argument("source_system")
@click.option("--entities", "-e", required=True, help="Target entities")
@click.option("--quiet", "-q", is_flag=True, help="Reduce verbosity")
def create_integration_guide(source_system: str, entities: str, quiet: bool):
    """Create an integration guide."""
    console.print(f"\n[bold blue]Creating integration guide for: {source_system}[/bold blue]\n")
    
    crew = get_crew(verbose=not quiet)
    result = crew.create_integration_guide(source_system, entities)
    
    console.print(Panel(str(result), title="Integration Guide", border_style="green"))


# =============================================================================
# GENERAL COMMANDS
# =============================================================================

@cli.command("ask")
@click.argument("question")
@click.option("--quiet", "-q", is_flag=True, help="Reduce verbosity")
def ask_question(question: str, quiet: bool):
    """Ask any question about Creatio CRM backend."""
    console.print(f"\n[bold blue]Question: {question}[/bold blue]\n")
    
    crew = get_crew(verbose=not quiet)
    result = crew.ask_question(question)
    
    console.print(Panel(str(result), title="Answer", border_style="green"))


@cli.command("analyze")
@click.argument("entity")
@click.option("--quiet", "-q", is_flag=True, help="Reduce verbosity")
def comprehensive_analysis(entity: str, quiet: bool):
    """Perform comprehensive analysis of an entity."""
    console.print(f"\n[bold blue]Comprehensive analysis of: {entity}[/bold blue]\n")
    
    crew = get_crew(verbose=not quiet)
    result = crew.comprehensive_entity_analysis(entity)
    
    console.print(Panel(str(result), title="Comprehensive Analysis", border_style="green"))


@cli.command("interactive")
def interactive_mode():
    """Start an interactive Q&A session."""
    console.print(Panel(
        "[bold]Creatio CRM Backend Analysis - Interactive Mode[/bold]\n\n"
        "Ask questions about Creatio CRM's schema, queries, or metrics.\n"
        "Type 'exit' or 'quit' to end the session.",
        title="Welcome",
        border_style="blue"
    ))
    
    crew = get_crew(verbose=False)
    
    while True:
        try:
            question = console.input("\n[bold green]Your question:[/bold green] ")
            
            if question.lower() in ['exit', 'quit', 'q']:
                console.print("\n[yellow]Goodbye![/yellow]\n")
                break
            
            if not question.strip():
                continue
            
            console.print("\n[dim]Thinking...[/dim]\n")
            result = crew.ask_question(question)
            
            console.print(Panel(str(result), title="Answer", border_style="green"))
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Session interrupted. Goodbye![/yellow]\n")
            break


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
