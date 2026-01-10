"""
Command-line interface for the DevLifecycle Crew.
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from devlifecycle_crew.crew import DevLifecycleCrew


console = Console()


@click.group()
@click.option('--verbose/--quiet', default=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, verbose):
    """DevLifecycle Crew - AI-powered SDLC management."""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose


@cli.command()
@click.argument('ticket_file', type=click.File('r'))
@click.pass_context
def triage(ctx, ticket_file):
    """Triage and process an incoming ticket."""
    ticket_data = ticket_file.read()
    
    console.print(Panel(
        "[bold blue]Processing Ticket[/bold blue]",
        subtitle="DevLifecycle Crew"
    ))
    
    crew = DevLifecycleCrew(verbose=ctx.obj['verbose'])
    result = crew.process_ticket(ticket_data)
    
    console.print("\n[bold green]Results:[/bold green]")
    console.print(Markdown(str(result)))


@cli.command()
@click.argument('requirements_file', type=click.File('r'))
@click.option('--stories/--no-stories', default=True, help='Create user stories')
@click.option('--validate/--no-validate', default=True, help='Validate requirements')
@click.pass_context
def analyze(ctx, requirements_file, stories, validate):
    """Analyze requirements from a file."""
    requirements_text = requirements_file.read()
    
    console.print(Panel(
        "[bold blue]Analyzing Requirements[/bold blue]",
        subtitle="DevLifecycle Crew"
    ))
    
    crew = DevLifecycleCrew(verbose=ctx.obj['verbose'])
    result = crew.analyze_requirements(
        requirements_text,
        create_stories=stories,
        validate=validate
    )
    
    console.print("\n[bold green]Results:[/bold green]")
    console.print(Markdown(str(result)))


@cli.command()
@click.argument('backlog_file', type=click.File('r'))
@click.option('--capacity', '-c', required=True, help='Team capacity (e.g., "40 story points")')
@click.option('--goal', '-g', required=True, help='Sprint goal')
@click.pass_context
def plan_sprint(ctx, backlog_file, capacity, goal):
    """Plan a sprint from backlog items."""
    backlog = backlog_file.read()
    
    console.print(Panel(
        "[bold blue]Planning Sprint[/bold blue]",
        subtitle="DevLifecycle Crew"
    ))
    
    crew = DevLifecycleCrew(verbose=ctx.obj['verbose'])
    result = crew.plan_sprint(backlog, capacity, goal)
    
    console.print("\n[bold green]Sprint Plan:[/bold green]")
    console.print(Markdown(str(result)))


@cli.command()
@click.argument('features_file', type=click.File('r'))
@click.option('--constraints', '-c', default='', help='Release constraints')
@click.option('--timeline', '-t', required=True, help='Timeline requirements')
@click.pass_context
def plan_release(ctx, features_file, constraints, timeline):
    """Plan a release from feature list."""
    features = features_file.read()
    
    console.print(Panel(
        "[bold blue]Planning Release[/bold blue]",
        subtitle="DevLifecycle Crew"
    ))
    
    crew = DevLifecycleCrew(verbose=ctx.obj['verbose'])
    result = crew.plan_release(features, constraints, timeline)
    
    console.print("\n[bold green]Release Plan:[/bold green]")
    console.print(Markdown(str(result)))


@cli.command()
@click.argument('project_file', type=click.File('r'))
@click.pass_context
def status(ctx, project_file):
    """Generate a project status report."""
    project_data = project_file.read()
    
    console.print(Panel(
        "[bold blue]Generating Status Report[/bold blue]",
        subtitle="DevLifecycle Crew"
    ))
    
    crew = DevLifecycleCrew(verbose=ctx.obj['verbose'])
    result = crew.generate_status_report(project_data)
    
    console.print("\n[bold green]Status Report:[/bold green]")
    console.print(Markdown(str(result)))


@cli.command()
@click.argument('change_file', type=click.File('r'))
@click.argument('state_file', type=click.File('r'))
@click.pass_context
def impact(ctx, change_file, state_file):
    """Assess the impact of a change request."""
    change_request = change_file.read()
    current_state = state_file.read()
    
    console.print(Panel(
        "[bold blue]Assessing Change Impact[/bold blue]",
        subtitle="DevLifecycle Crew"
    ))
    
    crew = DevLifecycleCrew(verbose=ctx.obj['verbose'])
    result = crew.assess_change_impact(change_request, current_state)
    
    console.print("\n[bold green]Impact Assessment:[/bold green]")
    console.print(Markdown(str(result)))


@cli.command()
@click.argument('requirements_file', type=click.File('r'))
@click.option('--context', '-c', default='', help='Project context')
@click.pass_context
def test_strategy(ctx, requirements_file, context):
    """Create a test strategy for requirements."""
    requirements = requirements_file.read()
    
    console.print(Panel(
        "[bold blue]Creating Test Strategy[/bold blue]",
        subtitle="DevLifecycle Crew"
    ))
    
    crew = DevLifecycleCrew(verbose=ctx.obj['verbose'])
    result = crew.create_test_strategy(requirements, context)
    
    console.print("\n[bold green]Test Strategy:[/bold green]")
    console.print(Markdown(str(result)))


@cli.command()
@click.argument('blockers_file', type=click.File('r'))
@click.pass_context
def blockers(ctx, blockers_file):
    """Analyze and plan resolution for blockers."""
    blockers_data = blockers_file.read()
    
    console.print(Panel(
        "[bold blue]Analyzing Blockers[/bold blue]",
        subtitle="DevLifecycle Crew"
    ))
    
    crew = DevLifecycleCrew(verbose=ctx.obj['verbose'])
    result = crew.manage_blockers(blockers_data)
    
    console.print("\n[bold green]Blocker Resolution Plan:[/bold green]")
    console.print(Markdown(str(result)))


@cli.command()
@click.argument('deliverables_file', type=click.File('r'))
@click.argument('criteria_file', type=click.File('r'))
@click.pass_context
def quality_gate(ctx, deliverables_file, criteria_file):
    """Perform a quality gate check."""
    deliverables = deliverables_file.read()
    criteria = criteria_file.read()
    
    console.print(Panel(
        "[bold blue]Quality Gate Check[/bold blue]",
        subtitle="DevLifecycle Crew"
    ))
    
    crew = DevLifecycleCrew(verbose=ctx.obj['verbose'])
    result = crew.quality_gate_check(deliverables, criteria)
    
    console.print("\n[bold green]Quality Gate Assessment:[/bold green]")
    console.print(Markdown(str(result)))


@cli.command()
@click.pass_context
def interactive(ctx):
    """Start an interactive session."""
    console.print(Panel(
        "[bold blue]DevLifecycle Crew - Interactive Mode[/bold blue]\n\n"
        "Available commands:\n"
        "  triage <text>     - Triage a ticket\n"
        "  analyze <text>    - Analyze requirements\n"
        "  status <text>     - Generate status report\n"
        "  help              - Show this help\n"
        "  exit              - Exit interactive mode",
        subtitle="Type 'help' for commands"
    ))
    
    crew = DevLifecycleCrew(verbose=ctx.obj['verbose'])
    
    while True:
        try:
            user_input = console.input("\n[bold cyan]> [/bold cyan]")
            
            if not user_input.strip():
                continue
            
            parts = user_input.strip().split(maxsplit=1)
            command = parts[0].lower()
            
            if command == 'exit' or command == 'quit':
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            if command == 'help':
                console.print(
                    "Commands: triage, analyze, status, help, exit"
                )
                continue
            
            if len(parts) < 2:
                console.print("[red]Please provide input text[/red]")
                continue
            
            text = parts[1]
            
            if command == 'triage':
                result = crew.process_ticket(text)
            elif command == 'analyze':
                result = crew.analyze_requirements(text)
            elif command == 'status':
                result = crew.generate_status_report(text)
            else:
                console.print(f"[red]Unknown command: {command}[/red]")
                continue
            
            console.print(Markdown(str(result)))
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


def main():
    """Entry point for the CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()
