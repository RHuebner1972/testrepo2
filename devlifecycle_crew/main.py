"""
Main entry point for the DevLifecycle Crew.

This module provides a simple programmatic interface for using the crew.
"""

from devlifecycle_crew.crew import DevLifecycleCrew


def run_example():
    """Run an example workflow demonstrating the crew capabilities."""
    
    print("=" * 60)
    print("DevLifecycle Crew - Example Workflow")
    print("=" * 60)
    
    # Initialize the crew
    crew = DevLifecycleCrew(verbose=True)
    
    # Example 1: Process a ticket
    print("\n" + "=" * 60)
    print("Example 1: Processing an Incoming Ticket")
    print("=" * 60)
    
    sample_ticket = """
    Title: Login page not loading on mobile devices
    
    Description:
    Users are reporting that the login page fails to load properly 
    on mobile devices (both iOS and Android). The page shows a blank 
    white screen. This started happening after the last deployment.
    
    Steps to reproduce:
    1. Open the app on a mobile device
    2. Navigate to the login page
    3. Page shows blank white screen
    
    Expected: Login page should display normally
    Actual: Blank white screen
    
    Affected users: ~500 daily active mobile users
    Workaround: Users can log in via desktop browser
    
    Reporter: support@example.com
    Date: 2026-01-10
    """
    
    result = crew.process_ticket(sample_ticket)
    print("\nTicket Processing Result:")
    print(result)
    
    # Example 2: Analyze requirements
    print("\n" + "=" * 60)
    print("Example 2: Analyzing Requirements")
    print("=" * 60)
    
    sample_requirements = """
    Feature: User Dashboard Enhancement
    
    Business Need:
    Users need a centralized dashboard to view their activity, 
    manage settings, and access key features quickly.
    
    Requirements:
    1. Display user's recent activity (last 7 days)
    2. Show summary statistics (total projects, tasks completed)
    3. Quick access to frequently used features
    4. Customizable widget layout
    5. Dark mode support
    6. Mobile responsive design
    7. Real-time updates without page refresh
    8. Export dashboard data to PDF
    
    Constraints:
    - Must work on all modern browsers
    - Page load time under 3 seconds
    - Support for 10,000 concurrent users
    """
    
    result = crew.analyze_requirements(
        sample_requirements, 
        create_stories=True, 
        validate=True
    )
    print("\nRequirements Analysis Result:")
    print(result)
    
    # Example 3: Plan a sprint
    print("\n" + "=" * 60)
    print("Example 3: Planning a Sprint")
    print("=" * 60)
    
    backlog = """
    Backlog Items:
    1. US-001: User authentication redesign (8 points)
    2. US-002: Dashboard widgets (5 points)
    3. US-003: API rate limiting (3 points)
    4. US-004: Search functionality (8 points)
    5. US-005: Export to PDF (5 points)
    6. BUG-001: Fix mobile login issue (3 points)
    7. BUG-002: Performance optimization (5 points)
    8. TECH-001: Database migration (8 points)
    """
    
    team_capacity = """
    Team: 5 developers
    Sprint Duration: 2 weeks (10 working days)
    Available Capacity: 40 story points
    Notes: 
    - One developer on vacation first week
    - Sprint includes quarterly planning meeting (4 hours)
    """
    
    sprint_goal = "Complete user authentication redesign and fix critical bugs"
    
    result = crew.plan_sprint(backlog, team_capacity, sprint_goal)
    print("\nSprint Plan Result:")
    print(result)
    
    print("\n" + "=" * 60)
    print("Example workflow completed!")
    print("=" * 60)


def main():
    """Main entry point."""
    run_example()


if __name__ == "__main__":
    main()
