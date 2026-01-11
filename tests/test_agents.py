"""
Tests for agent creation and configuration.
"""

import pytest
from unittest.mock import patch, MagicMock


class TestAgentCreation:
    """Test agent creation and configuration."""
    
    def test_intake_agent_imports(self):
        """Test that IntakeAgent can be imported."""
        from devlifecycle_crew.agents import IntakeAgent
        assert IntakeAgent is not None
    
    def test_requirements_agent_imports(self):
        """Test that RequirementsAgent can be imported."""
        from devlifecycle_crew.agents import RequirementsAgent
        assert RequirementsAgent is not None
    
    def test_sdlc_manager_agent_imports(self):
        """Test that SDLCManagerAgent can be imported."""
        from devlifecycle_crew.agents import SDLCManagerAgent
        assert SDLCManagerAgent is not None
    
    def test_quality_agent_imports(self):
        """Test that QualityAgent can be imported."""
        from devlifecycle_crew.agents import QualityAgent
        assert QualityAgent is not None
    
    def test_planning_agent_imports(self):
        """Test that PlanningAgent can be imported."""
        from devlifecycle_crew.agents import PlanningAgent
        assert PlanningAgent is not None


class TestAgentConfiguration:
    """Test agent configuration."""
    
    @patch('devlifecycle_crew.agents.intake_agent.Agent')
    def test_intake_agent_has_correct_role(self, mock_agent):
        """Test IntakeAgent has correct role configured."""
        from devlifecycle_crew.agents import IntakeAgent
        
        mock_agent.return_value = MagicMock()
        agent = IntakeAgent.create()
        
        # Verify Agent was called
        mock_agent.assert_called_once()
        call_kwargs = mock_agent.call_args.kwargs
        
        assert "Intake" in call_kwargs.get('role', '') or "Ticket" in call_kwargs.get('role', '')
    
    @patch('devlifecycle_crew.agents.requirements_agent.Agent')
    def test_requirements_agent_has_correct_role(self, mock_agent):
        """Test RequirementsAgent has correct role configured."""
        from devlifecycle_crew.agents import RequirementsAgent
        
        mock_agent.return_value = MagicMock()
        agent = RequirementsAgent.create()
        
        mock_agent.assert_called_once()
        call_kwargs = mock_agent.call_args.kwargs
        
        assert "Requirements" in call_kwargs.get('role', '')
    
    @patch('devlifecycle_crew.agents.sdlc_manager_agent.Agent')
    def test_sdlc_manager_agent_has_correct_role(self, mock_agent):
        """Test SDLCManagerAgent has correct role configured."""
        from devlifecycle_crew.agents import SDLCManagerAgent
        
        mock_agent.return_value = MagicMock()
        agent = SDLCManagerAgent.create()
        
        mock_agent.assert_called_once()
        call_kwargs = mock_agent.call_args.kwargs
        
        assert "SDLC" in call_kwargs.get('role', '') or "Manager" in call_kwargs.get('role', '')
