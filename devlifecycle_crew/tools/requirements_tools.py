"""
Requirements management tools for the DevLifecycle Crew.
"""

from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class RequirementsInput(BaseModel):
    """Input schema for requirements parsing."""
    text: str = Field(description="Raw text containing requirements to parse")
    format: str = Field(
        default="auto",
        description="Expected format: auto, user_story, technical, business"
    )


class RequirementsValidationInput(BaseModel):
    """Input schema for requirements validation."""
    requirements: str = Field(description="Requirements to validate")
    validation_type: str = Field(
        default="full",
        description="Type of validation: full, testability, completeness, consistency"
    )


class TraceabilityInput(BaseModel):
    """Input schema for traceability operations."""
    requirement_id: str = Field(description="Requirement ID to trace")
    direction: str = Field(
        default="both",
        description="Trace direction: forward, backward, both"
    )


class RequirementsParserTool(BaseTool):
    """Tool for parsing requirements from text."""
    
    name: str = "requirements_parser"
    description: str = (
        "Parses raw text to extract structured requirements. "
        "Can identify user stories, functional requirements, "
        "non-functional requirements, and acceptance criteria. "
        "Supports various input formats."
    )
    args_schema: Type[BaseModel] = RequirementsInput
    
    def _run(self, text: str, format: str = "auto") -> str:
        """Parse requirements from text."""
        # In a real implementation, this would use NLP to extract requirements
        # This is a structured mock implementation
        
        parsed = {
            "success": True,
            "format_detected": format if format != "auto" else "mixed",
            "requirements_found": {
                "functional": [
                    {
                        "id": "FR-001",
                        "statement": "System shall allow users to submit tickets",
                        "priority": "must-have",
                        "source": "Extracted from input text"
                    }
                ],
                "non_functional": [
                    {
                        "id": "NFR-001",
                        "statement": "System shall respond within 2 seconds",
                        "category": "performance",
                        "priority": "should-have"
                    }
                ],
                "user_stories": [
                    {
                        "id": "US-001",
                        "as_a": "developer",
                        "i_want": "to track my tasks",
                        "so_that": "I can manage my work effectively"
                    }
                ],
                "acceptance_criteria": [
                    {
                        "id": "AC-001",
                        "given": "a logged-in user",
                        "when": "they submit a ticket",
                        "then": "the ticket is created in the system"
                    }
                ]
            },
            "parsing_notes": [
                "Found requirements-like statements in input",
                "Some statements may need clarification"
            ]
        }
        
        return str(parsed)


class RequirementsValidatorTool(BaseTool):
    """Tool for validating requirements quality."""
    
    name: str = "requirements_validator"
    description: str = (
        "Validates requirements for quality attributes including "
        "testability, completeness, consistency, and clarity. "
        "Returns a validation report with issues and recommendations."
    )
    args_schema: Type[BaseModel] = RequirementsValidationInput
    
    def _run(self, requirements: str, validation_type: str = "full") -> str:
        """Validate requirements."""
        # In a real implementation, this would perform actual validation
        
        validation_result = {
            "success": True,
            "validation_type": validation_type,
            "overall_score": 7.5,
            "max_score": 10,
            "checks": {
                "testability": {
                    "score": 8,
                    "issues": ["Some requirements lack measurable criteria"],
                    "passed": True
                },
                "completeness": {
                    "score": 7,
                    "issues": ["Missing error handling scenarios"],
                    "passed": True
                },
                "consistency": {
                    "score": 9,
                    "issues": [],
                    "passed": True
                },
                "clarity": {
                    "score": 6,
                    "issues": ["Ambiguous term 'quickly' needs definition"],
                    "passed": False
                }
            },
            "recommendations": [
                "Add specific metrics for performance requirements",
                "Define 'quickly' with measurable time bounds",
                "Add error handling requirements"
            ],
            "ready_for_development": True,
            "conditions": ["Address clarity issues before sprint start"]
        }
        
        return str(validation_result)


class TraceabilityMatrixTool(BaseTool):
    """Tool for requirements traceability."""
    
    name: str = "traceability_matrix"
    description: str = (
        "Creates and queries requirements traceability. "
        "Links requirements to source documents, design artifacts, "
        "test cases, and code. Supports forward and backward tracing."
    )
    args_schema: Type[BaseModel] = TraceabilityInput
    
    def _run(
        self,
        requirement_id: str,
        direction: str = "both"
    ) -> str:
        """Get traceability information for a requirement."""
        # In a real implementation, this would query a traceability database
        
        trace_result = {
            "success": True,
            "requirement_id": requirement_id,
            "direction": direction,
            "traces": {
                "backward": {
                    "business_need": "BN-001: Improve developer productivity",
                    "source_ticket": "TICKET-123",
                    "stakeholder": "Product Owner"
                },
                "forward": {
                    "user_stories": ["US-001", "US-002"],
                    "design_docs": ["DESIGN-001"],
                    "test_cases": ["TC-001", "TC-002", "TC-003"],
                    "code_modules": ["ticket_service.py", "ticket_api.py"]
                }
            },
            "coverage": {
                "has_source": True,
                "has_design": True,
                "has_tests": True,
                "has_code": True,
                "fully_traced": True
            }
        }
        
        return str(trace_result)
