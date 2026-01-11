"""
Example usage of the Creatio CRM Backend Analysis Crew.

This file demonstrates various ways to use the crew to analyze
the Creatio CRM backend.
"""

from creatio_crm_crew import CreatioCRMCrew


def example_schema_exploration():
    """Example: Exploring the Creatio CRM schema."""
    print("\n" + "=" * 60)
    print("Example: Schema Exploration")
    print("=" * 60)
    
    crew = CreatioCRMCrew(verbose=True)
    
    # Explore a specific entity
    print("\n1. Exploring the Contact entity:")
    print("-" * 40)
    result = crew.explore_entity("Contact")
    print(result)
    
    # Analyze relationships
    print("\n2. Analyzing Contact-Account relationships:")
    print("-" * 40)
    result = crew.analyze_relationships("Contact", "Account")
    print(result)
    
    # Get schema overview
    print("\n3. Getting full schema overview:")
    print("-" * 40)
    result = crew.get_schema_overview()
    print(result)


def example_query_building():
    """Example: Building queries for Creatio data."""
    print("\n" + "=" * 60)
    print("Example: Query Building")
    print("=" * 60)
    
    crew = CreatioCRMCrew(verbose=True)
    
    # Build a query from a business question
    print("\n1. Building query from business question:")
    print("-" * 40)
    result = crew.build_query(
        "Show me all open opportunities over $10,000 with their account names"
    )
    print(result)
    
    # Build a report query
    print("\n2. Building report query:")
    print("-" * 40)
    result = crew.build_report_query(
        report_description="Sales by account industry",
        entities="Opportunity, Account",
        time_range="this quarter"
    )
    print(result)
    
    # Build OData query
    print("\n3. Building OData API query:")
    print("-" * 40)
    result = crew.build_odata_query(
        entity="Contact",
        requirements="Get contacts with their account info, filter by active status"
    )
    print(result)


def example_metrics_and_kpis():
    """Example: Working with metrics and KPIs."""
    print("\n" + "=" * 60)
    print("Example: Metrics and KPIs")
    print("=" * 60)
    
    crew = CreatioCRMCrew(verbose=True)
    
    # Define KPIs for a business goal
    print("\n1. Defining KPIs for sales performance:")
    print("-" * 40)
    result = crew.define_kpis(
        business_goal="Improve sales team performance",
        context="B2B software company, 20 sales reps, quarterly targets"
    )
    print(result)
    
    # Recommend metrics for a role
    print("\n2. Recommending metrics for sales manager:")
    print("-" * 40)
    result = crew.recommend_metrics(
        role="manager",
        focus_area="sales pipeline"
    )
    print(result)
    
    # Design a dashboard
    print("\n3. Designing executive dashboard:")
    print("-" * 40)
    result = crew.design_dashboard(
        purpose="Executive overview of sales and customer health",
        audience="executive"
    )
    print(result)
    
    # Analyze sales pipeline
    print("\n4. Analyzing sales pipeline:")
    print("-" * 40)
    result = crew.analyze_sales_pipeline(depth="standard")
    print(result)


def example_documentation():
    """Example: Generating documentation."""
    print("\n" + "=" * 60)
    print("Example: Documentation Generation")
    print("=" * 60)
    
    crew = CreatioCRMCrew(verbose=True)
    
    # Generate documentation for entities
    print("\n1. Generating documentation for core entities:")
    print("-" * 40)
    result = crew.generate_documentation(entities="Contact, Account, Opportunity")
    print(result)
    
    # Create data dictionary
    print("\n2. Creating data dictionary for Opportunity:")
    print("-" * 40)
    result = crew.create_data_dictionary("Opportunity")
    print(result)
    
    # Generate ERD
    print("\n3. Generating ERD:")
    print("-" * 40)
    result = crew.generate_erd(
        entities="Contact, Account, Opportunity, Lead",
        include_columns=True
    )
    print(result)
    
    # Create integration guide
    print("\n4. Creating integration guide:")
    print("-" * 40)
    result = crew.create_integration_guide(
        source_system="Salesforce",
        target_entities="Contact, Account, Opportunity"
    )
    print(result)


def example_ask_questions():
    """Example: Asking ad-hoc questions."""
    print("\n" + "=" * 60)
    print("Example: Asking Questions")
    print("=" * 60)
    
    crew = CreatioCRMCrew(verbose=True)
    
    questions = [
        "What tables store customer information in Creatio?",
        "How do I query opportunities closing this month?",
        "What KPIs should I track for customer service?",
        "How is the Activity entity related to Contacts and Accounts?",
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. Question: {question}")
        print("-" * 40)
        result = crew.ask_question(question)
        print(result)
        print()


def example_comprehensive_analysis():
    """Example: Comprehensive entity analysis."""
    print("\n" + "=" * 60)
    print("Example: Comprehensive Analysis")
    print("=" * 60)
    
    crew = CreatioCRMCrew(verbose=True)
    
    print("\nPerforming comprehensive analysis of Opportunity entity:")
    print("-" * 40)
    result = crew.comprehensive_entity_analysis("Opportunity")
    print(result)


def example_full_metrics_analysis():
    """Example: Full metrics analysis for a business area."""
    print("\n" + "=" * 60)
    print("Example: Full Metrics Analysis")
    print("=" * 60)
    
    crew = CreatioCRMCrew(verbose=True)
    
    print("\nPerforming full metrics analysis for sales:")
    print("-" * 40)
    result = crew.full_metrics_analysis(
        business_area="sales",
        audience="manager"
    )
    print(result)


def main():
    """Run all examples."""
    print("\n" + "#" * 60)
    print("# Creatio CRM Backend Analysis Crew - Examples")
    print("#" * 60)
    
    # Note: Each example can be run independently
    # Uncomment the ones you want to run
    
    # Schema exploration examples
    example_schema_exploration()
    
    # Query building examples
    # example_query_building()
    
    # Metrics and KPI examples
    # example_metrics_and_kpis()
    
    # Documentation examples
    # example_documentation()
    
    # Ad-hoc question examples
    # example_ask_questions()
    
    # Comprehensive analysis
    # example_comprehensive_analysis()
    
    # Full metrics analysis
    # example_full_metrics_analysis()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
