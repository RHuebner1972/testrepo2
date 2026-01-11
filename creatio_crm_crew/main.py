"""
Main entry point for Creatio CRM Backend Analysis Crew.

This module provides a simple way to use the crew programmatically.
"""

from creatio_crm_crew.crew import CreatioCRMCrew


def main():
    """Main function demonstrating crew usage."""
    # Initialize the crew
    crew = CreatioCRMCrew(verbose=True)
    
    print("=" * 60)
    print("Creatio CRM Backend Analysis Crew")
    print("=" * 60)
    print()
    
    # Example: Ask a general question
    print("Example: Asking about Contact entity...")
    print("-" * 40)
    
    result = crew.ask_question(
        "What are the key fields in the Contact entity and how does it relate to Account?"
    )
    
    print(result)


if __name__ == "__main__":
    main()
