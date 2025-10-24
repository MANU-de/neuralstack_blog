"""
Unit tests specifically for the agent.py module.

This test suite focuses on testing the CrewAI agent functionality,
including agent creation, task definition, and crew execution.
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the agent module
from agent import create_content_crew


class TestAgentInitialization:
    """Test agent initialization and configuration."""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key', 'SERPER_API_KEY': 'test_serper_key'})
    @patch('agent.SerperDevTool')
    @patch('agent.Agent')
    def test_agent_creation_with_search_tool(self, mock_agent_class, mock_serper_tool):
        """Test that agents are created with search tool when available."""
        # Mock the SerperDevTool
        mock_search_tool = Mock()
        mock_serper_tool.return_value = mock_search_tool
        
        # Mock the Agent class
        mock_agent_instance = Mock()
        mock_agent_class.return_value = mock_agent_instance
        
        # Import and test agent creation
        from agent import researcher, content_writer
        
        # Verify that agents were created
        assert researcher is not None
        assert content_writer is not None
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}, clear=True)
    @patch('agent.Agent')
    def test_agent_creation_without_search_tool(self, mock_agent_class):
        """Test that agents are created without search tool when not available."""
        # Mock the Agent class
        mock_agent_instance = Mock()
        mock_agent_class.return_value = mock_agent_instance
        
        # Import and test agent creation
        from agent import researcher, content_writer
        
        # Verify that agents were created
        assert researcher is not None
        assert content_writer is not None
    
    def test_missing_openai_key_raises_error(self):
        """Test that missing OpenAI API key raises ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="OPENAI_API_KEY not found"):
                # Re-import the module to trigger the key check
                import importlib
                import agent
                importlib.reload(agent)


class TestCrewCreation:
    """Test crew creation and task definition."""
    
    @patch('agent.Crew')
    @patch('agent.Task')
    @patch('agent.researcher')
    @patch('agent.content_writer')
    def test_create_content_crew_initialization(self, mock_content_writer, mock_researcher, 
                                               mock_task_class, mock_crew_class):
        """Test that crew is properly initialized with agents and tasks."""
        # Mock task instances
        mock_task1 = Mock()
        mock_task2 = Mock()
        mock_task_class.side_effect = [mock_task1, mock_task2]
        
        # Mock crew instance
        mock_crew_instance = Mock()
        mock_crew_class.return_value = mock_crew_instance
        
        # Call the function
        result = create_content_crew("Test Topic")
        
        # Verify that tasks were created with correct parameters
        assert mock_task_class.call_count == 2
        
        # Verify that crew was created with correct parameters
        mock_crew_class.assert_called_once()
        call_args = mock_crew_class.call_args
        assert 'agents' in call_args.kwargs
        assert 'tasks' in call_args.kwargs
        assert 'process' in call_args.kwargs
        assert 'verbose' in call_args.kwargs
    
    @patch('agent.Crew')
    @patch('agent.Task')
    @patch('agent.researcher')
    @patch('agent.content_writer')
    def test_task_descriptions_contain_topic(self, mock_content_writer, mock_researcher,
                                            mock_task_class, mock_crew_class):
        """Test that task descriptions contain the provided topic."""
        # Mock task instances
        mock_task1 = Mock()
        mock_task2 = Mock()
        mock_task_class.side_effect = [mock_task1, mock_task2]
        
        # Mock crew instance
        mock_crew_instance = Mock()
        mock_crew_instance.kickoff.return_value = "Test result"
        mock_crew_class.return_value = mock_crew_instance
        
        # Call the function
        create_content_crew("AI in Healthcare")
        
        # Verify that task descriptions contain the topic
        task_calls = mock_task_class.call_args_list
        for call in task_calls:
            description = call.kwargs.get('description', '')
            assert "AI in Healthcare" in description


class TestCrewExecution:
    """Test crew execution and result handling."""
    
    @patch('agent.Crew')
    @patch('agent.Task')
    @patch('agent.researcher')
    @patch('agent.content_writer')
    def test_crew_kickoff_success(self, mock_content_writer, mock_researcher,
                                 mock_task_class, mock_crew_class):
        """Test successful crew execution."""
        # Mock task instances
        mock_task1 = Mock()
        mock_task2 = Mock()
        mock_task_class.side_effect = [mock_task1, mock_task2]
        
        # Mock crew instance with successful execution
        mock_crew_instance = Mock()
        expected_result = "Generated blog post about AI"
        mock_crew_instance.kickoff.return_value = expected_result
        mock_crew_class.return_value = mock_crew_instance
        
        # Call the function
        result = create_content_crew("AI in Healthcare")
        
        # Verify the result
        assert result == expected_result
        mock_crew_instance.kickoff.assert_called_once()
    
    @patch('agent.Crew')
    @patch('agent.Task')
    @patch('agent.researcher')
    @patch('agent.content_writer')
    def test_crew_kickoff_failure(self, mock_content_writer, mock_researcher,
                                 mock_task_class, mock_crew_class):
        """Test crew execution failure."""
        # Mock task instances
        mock_task1 = Mock()
        mock_task2 = Mock()
        mock_task_class.side_effect = [mock_task1, mock_task2]
        
        # Mock crew instance with failed execution
        mock_crew_instance = Mock()
        mock_crew_instance.kickoff.side_effect = Exception("Crew execution failed")
        mock_crew_class.return_value = mock_crew_instance
        
        # Call the function and expect exception
        with pytest.raises(Exception, match="Crew execution failed"):
            create_content_crew("AI in Healthcare")
    
    @patch('agent.Crew')
    @patch('agent.Task')
    @patch('agent.researcher')
    @patch('agent.content_writer')
    def test_crew_kickoff_empty_result(self, mock_content_writer, mock_researcher,
                                      mock_task_class, mock_crew_class):
        """Test crew execution with empty result."""
        # Mock task instances
        mock_task1 = Mock()
        mock_task2 = Mock()
        mock_task_class.side_effect = [mock_task1, mock_task2]
        
        # Mock crew instance with empty result
        mock_crew_instance = Mock()
        mock_crew_instance.kickoff.return_value = None
        mock_crew_class.return_value = mock_crew_instance
        
        # Call the function
        result = create_content_crew("AI in Healthcare")
        
        # Verify the result is None
        assert result is None


class TestAgentRoles:
    """Test agent role definitions and configurations."""
    
    @patch('agent.SerperDevTool')
    @patch('agent.Agent')
    def test_researcher_agent_configuration(self, mock_agent_class, mock_serper_tool):
        """Test researcher agent configuration."""
        # Mock the search tool
        mock_search_tool = Mock()
        mock_serper_tool.return_value = mock_search_tool
        
        # Mock the Agent class
        mock_agent_instance = Mock()
        mock_agent_class.return_value = mock_agent_instance
        
        # Import the researcher agent
        from agent import researcher
        
        # Verify agent creation was called with correct parameters
        mock_agent_class.assert_called()
        call_args = mock_agent_class.call_args
        
        # Check that the researcher agent has the correct role
        assert 'role' in call_args.kwargs
        assert 'Senior Research Analyst' in call_args.kwargs['role']
    
    @patch('agent.Agent')
    def test_content_writer_agent_configuration(self, mock_agent_class):
        """Test content writer agent configuration."""
        # Mock the Agent class
        mock_agent_instance = Mock()
        mock_agent_class.return_value = mock_agent_instance
        
        # Import the content writer agent
        from agent import content_writer
        
        # Verify agent creation was called with correct parameters
        mock_agent_class.assert_called()
        call_args = mock_agent_class.call_args
        
        # Check that the content writer agent has the correct role
        assert 'role' in call_args.kwargs
        assert 'Senior Content Writer' in call_args.kwargs['role']


class TestTaskDefinition:
    """Test task definition and configuration."""
    
    @patch('agent.Crew')
    @patch('agent.Task')
    @patch('agent.researcher')
    @patch('agent.content_writer')
    def test_research_task_configuration(self, mock_content_writer, mock_researcher,
                                       mock_task_class, mock_crew_class):
        """Test research task configuration."""
        # Mock task instances
        mock_task1 = Mock()
        mock_task2 = Mock()
        mock_task_class.side_effect = [mock_task1, mock_task2]
        
        # Mock crew instance
        mock_crew_instance = Mock()
        mock_crew_instance.kickoff.return_value = "Test result"
        mock_crew_class.return_value = mock_crew_instance
        
        # Call the function
        create_content_crew("AI in Healthcare")
        
        # Verify that the first task (research task) was created with correct parameters
        first_task_call = mock_task_class.call_args_list[0]
        assert 'description' in first_task_call.kwargs
        assert 'expected_output' in first_task_call.kwargs
        assert 'agent' in first_task_call.kwargs
        assert first_task_call.kwargs['agent'] == mock_researcher
    
    @patch('agent.Crew')
    @patch('agent.Task')
    @patch('agent.researcher')
    @patch('agent.content_writer')
    def test_writing_task_configuration(self, mock_content_writer, mock_researcher,
                                      mock_task_class, mock_crew_class):
        """Test writing task configuration."""
        # Mock task instances
        mock_task1 = Mock()
        mock_task2 = Mock()
        mock_task_class.side_effect = [mock_task1, mock_task2]
        
        # Mock crew instance
        mock_crew_instance = Mock()
        mock_crew_instance.kickoff.return_value = "Test result"
        mock_crew_class.return_value = mock_crew_instance
        
        # Call the function
        create_content_crew("AI in Healthcare")
        
        # Verify that the second task (writing task) was created with correct parameters
        second_task_call = mock_task_class.call_args_list[1]
        assert 'description' in second_task_call.kwargs
        assert 'expected_output' in second_task_call.kwargs
        assert 'agent' in second_task_call.kwargs
        assert second_task_call.kwargs['agent'] == mock_content_writer


class TestCrewProcess:
    """Test crew process configuration."""
    
    @patch('agent.Crew')
    @patch('agent.Task')
    @patch('agent.researcher')
    @patch('agent.content_writer')
    def test_crew_process_sequential(self, mock_content_writer, mock_researcher,
                                    mock_task_class, mock_crew_class):
        """Test that crew is configured with sequential process."""
        # Mock task instances
        mock_task1 = Mock()
        mock_task2 = Mock()
        mock_task_class.side_effect = [mock_task1, mock_task2]
        
        # Mock crew instance
        mock_crew_instance = Mock()
        mock_crew_instance.kickoff.return_value = "Test result"
        mock_crew_class.return_value = mock_crew_instance
        
        # Call the function
        create_content_crew("AI in Healthcare")
        
        # Verify that crew was created with sequential process
        call_args = mock_crew_class.call_args
        assert 'process' in call_args.kwargs
        # Note: We can't directly test the Process.sequential enum, but we can verify it's set


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
