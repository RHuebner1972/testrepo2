"""
Tests for custom tools.
"""

import pytest


class TestTicketTools:
    """Test ticket management tools."""
    
    def test_ticket_creator_tool_imports(self):
        """Test TicketCreatorTool can be imported."""
        from devlifecycle_crew.tools import TicketCreatorTool
        assert TicketCreatorTool is not None
    
    def test_ticket_creator_creates_ticket(self):
        """Test TicketCreatorTool creates a ticket."""
        from devlifecycle_crew.tools import TicketCreatorTool
        
        tool = TicketCreatorTool()
        result = tool._run(
            title="Test Ticket",
            description="Test description",
            ticket_type="bug",
            priority="high"
        )
        
        assert "success" in result.lower() or "ticket" in result.lower()
        assert "TICKET-" in result.upper()
    
    def test_ticket_search_tool_imports(self):
        """Test TicketSearchTool can be imported."""
        from devlifecycle_crew.tools import TicketSearchTool
        assert TicketSearchTool is not None
    
    def test_ticket_search_returns_results(self):
        """Test TicketSearchTool returns search results."""
        from devlifecycle_crew.tools import TicketSearchTool
        
        tool = TicketSearchTool()
        result = tool._run(query="login bug", status="open")
        
        assert "success" in result.lower()
        assert "results" in result.lower() or "tickets" in result.lower()
    
    def test_ticket_updater_tool_imports(self):
        """Test TicketUpdaterTool can be imported."""
        from devlifecycle_crew.tools import TicketUpdaterTool
        assert TicketUpdaterTool is not None
    
    def test_ticket_updater_updates_field(self):
        """Test TicketUpdaterTool updates a ticket field."""
        from devlifecycle_crew.tools import TicketUpdaterTool
        
        tool = TicketUpdaterTool()
        result = tool._run(
            ticket_id="TICKET-001",
            field="status",
            value="in_progress"
        )
        
        assert "success" in result.lower()


class TestRequirementsTools:
    """Test requirements management tools."""
    
    def test_requirements_parser_imports(self):
        """Test RequirementsParserTool can be imported."""
        from devlifecycle_crew.tools import RequirementsParserTool
        assert RequirementsParserTool is not None
    
    def test_requirements_parser_parses_text(self):
        """Test RequirementsParserTool parses requirements."""
        from devlifecycle_crew.tools import RequirementsParserTool
        
        tool = RequirementsParserTool()
        result = tool._run(
            text="The system shall allow users to log in with email and password."
        )
        
        assert "success" in result.lower()
        assert "requirements" in result.lower()
    
    def test_requirements_validator_imports(self):
        """Test RequirementsValidatorTool can be imported."""
        from devlifecycle_crew.tools import RequirementsValidatorTool
        assert RequirementsValidatorTool is not None
    
    def test_requirements_validator_validates(self):
        """Test RequirementsValidatorTool validates requirements."""
        from devlifecycle_crew.tools import RequirementsValidatorTool
        
        tool = RequirementsValidatorTool()
        result = tool._run(
            requirements="FR-001: System shall authenticate users"
        )
        
        assert "success" in result.lower()
        assert "score" in result.lower()
    
    def test_traceability_matrix_imports(self):
        """Test TraceabilityMatrixTool can be imported."""
        from devlifecycle_crew.tools import TraceabilityMatrixTool
        assert TraceabilityMatrixTool is not None


class TestSDLCTools:
    """Test SDLC management tools."""
    
    def test_sprint_planner_imports(self):
        """Test SprintPlannerTool can be imported."""
        from devlifecycle_crew.tools import SprintPlannerTool
        assert SprintPlannerTool is not None
    
    def test_sprint_planner_creates_plan(self):
        """Test SprintPlannerTool creates a sprint plan."""
        from devlifecycle_crew.tools import SprintPlannerTool
        
        tool = SprintPlannerTool()
        result = tool._run(
            sprint_name="Sprint 12",
            capacity=40,
            items="US-001, US-002, US-003"
        )
        
        assert "success" in result.lower()
        assert "sprint" in result.lower()
    
    def test_status_tracker_imports(self):
        """Test StatusTrackerTool can be imported."""
        from devlifecycle_crew.tools import StatusTrackerTool
        assert StatusTrackerTool is not None
    
    def test_status_tracker_returns_status(self):
        """Test StatusTrackerTool returns project status."""
        from devlifecycle_crew.tools import StatusTrackerTool
        
        tool = StatusTrackerTool()
        result = tool._run(project_id="test-project")
        
        assert "success" in result.lower()
        assert "health" in result.lower() or "status" in result.lower()
    
    def test_risk_assessment_imports(self):
        """Test RiskAssessmentTool can be imported."""
        from devlifecycle_crew.tools import RiskAssessmentTool
        assert RiskAssessmentTool is not None
    
    def test_risk_assessment_assesses_risks(self):
        """Test RiskAssessmentTool assesses risks."""
        from devlifecycle_crew.tools import RiskAssessmentTool
        
        tool = RiskAssessmentTool()
        result = tool._run(
            scope="sprint",
            context="Sprint 12 with new features"
        )
        
        assert "success" in result.lower()
        assert "risk" in result.lower()
