"""
Tests for the main DevLifecycle Crew.
"""

import pytest
from unittest.mock import patch, MagicMock


class TestCrewInitialization:
    """Test crew initialization."""
    
    def test_crew_imports(self):
        """Test DevLifecycleCrew can be imported."""
        from devlifecycle_crew import DevLifecycleCrew
        assert DevLifecycleCrew is not None
    
    @patch('devlifecycle_crew.crew.IntakeAgent')
    @patch('devlifecycle_crew.crew.RequirementsAgent')
    @patch('devlifecycle_crew.crew.SDLCManagerAgent')
    @patch('devlifecycle_crew.crew.QualityAgent')
    @patch('devlifecycle_crew.crew.PlanningAgent')
    def test_crew_initializes_all_agents(
        self, 
        mock_planning, 
        mock_quality, 
        mock_sdlc, 
        mock_requirements, 
        mock_intake
    ):
        """Test crew initializes all required agents."""
        # Setup mocks
        for mock in [mock_planning, mock_quality, mock_sdlc, mock_requirements, mock_intake]:
            mock.create.return_value = MagicMock()
        
        from devlifecycle_crew import DevLifecycleCrew
        
        crew = DevLifecycleCrew(verbose=False)
        
        # Verify all agents were created
        mock_intake.create.assert_called_once()
        mock_requirements.create.assert_called_once()
        mock_sdlc.create.assert_called_once()
        mock_quality.create.assert_called_once()
        mock_planning.create.assert_called_once()
    
    @patch('devlifecycle_crew.crew.IntakeAgent')
    @patch('devlifecycle_crew.crew.RequirementsAgent')
    @patch('devlifecycle_crew.crew.SDLCManagerAgent')
    @patch('devlifecycle_crew.crew.QualityAgent')
    @patch('devlifecycle_crew.crew.PlanningAgent')
    def test_crew_has_tools(
        self,
        mock_planning,
        mock_quality,
        mock_sdlc,
        mock_requirements,
        mock_intake
    ):
        """Test crew initializes with required tools."""
        for mock in [mock_planning, mock_quality, mock_sdlc, mock_requirements, mock_intake]:
            mock.create.return_value = MagicMock()
        
        from devlifecycle_crew import DevLifecycleCrew
        
        crew = DevLifecycleCrew(verbose=False)
        
        assert len(crew.ticket_tools) > 0
        assert len(crew.requirements_tools) > 0
        assert len(crew.sdlc_tools) > 0


class TestCrewMethods:
    """Test crew workflow methods."""
    
    def test_crew_has_process_ticket_method(self):
        """Test crew has process_ticket method."""
        from devlifecycle_crew import DevLifecycleCrew
        
        assert hasattr(DevLifecycleCrew, 'process_ticket')
    
    def test_crew_has_analyze_requirements_method(self):
        """Test crew has analyze_requirements method."""
        from devlifecycle_crew import DevLifecycleCrew
        
        assert hasattr(DevLifecycleCrew, 'analyze_requirements')
    
    def test_crew_has_plan_sprint_method(self):
        """Test crew has plan_sprint method."""
        from devlifecycle_crew import DevLifecycleCrew
        
        assert hasattr(DevLifecycleCrew, 'plan_sprint')
    
    def test_crew_has_plan_release_method(self):
        """Test crew has plan_release method."""
        from devlifecycle_crew import DevLifecycleCrew
        
        assert hasattr(DevLifecycleCrew, 'plan_release')
    
    def test_crew_has_generate_status_report_method(self):
        """Test crew has generate_status_report method."""
        from devlifecycle_crew import DevLifecycleCrew
        
        assert hasattr(DevLifecycleCrew, 'generate_status_report')
    
    def test_crew_has_assess_change_impact_method(self):
        """Test crew has assess_change_impact method."""
        from devlifecycle_crew import DevLifecycleCrew
        
        assert hasattr(DevLifecycleCrew, 'assess_change_impact')
    
    def test_crew_has_create_test_strategy_method(self):
        """Test crew has create_test_strategy method."""
        from devlifecycle_crew import DevLifecycleCrew
        
        assert hasattr(DevLifecycleCrew, 'create_test_strategy')
    
    def test_crew_has_full_workflow_method(self):
        """Test crew has full_ticket_to_sprint_workflow method."""
        from devlifecycle_crew import DevLifecycleCrew
        
        assert hasattr(DevLifecycleCrew, 'full_ticket_to_sprint_workflow')


class TestCrewConfiguration:
    """Test crew configuration options."""
    
    @patch('devlifecycle_crew.crew.IntakeAgent')
    @patch('devlifecycle_crew.crew.RequirementsAgent')
    @patch('devlifecycle_crew.crew.SDLCManagerAgent')
    @patch('devlifecycle_crew.crew.QualityAgent')
    @patch('devlifecycle_crew.crew.PlanningAgent')
    def test_crew_verbose_setting(
        self,
        mock_planning,
        mock_quality,
        mock_sdlc,
        mock_requirements,
        mock_intake
    ):
        """Test crew respects verbose setting."""
        for mock in [mock_planning, mock_quality, mock_sdlc, mock_requirements, mock_intake]:
            mock.create.return_value = MagicMock()
        
        from devlifecycle_crew import DevLifecycleCrew
        
        crew_verbose = DevLifecycleCrew(verbose=True)
        assert crew_verbose.verbose is True
        
        crew_quiet = DevLifecycleCrew(verbose=False)
        assert crew_quiet.verbose is False
