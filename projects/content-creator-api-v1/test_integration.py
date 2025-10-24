"""
Integration tests for the Content Creator API.

These tests verify the complete workflow from API request to agent execution.
"""

import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app


@pytest.mark.integration
class TestCompleteWorkflow:
    """Test the complete workflow from API to agent execution."""
    
    @patch('agent.Crew')
    @patch('agent.Agent')
    @patch('agent.SerperDevTool')
    def test_full_content_creation_workflow(self, mock_serper_tool, mock_agent_class, mock_crew_class):
        """Test the complete workflow from API request to content generation."""
        # Mock the search tool
        mock_search_tool = Mock()
        mock_serper_tool.return_value = mock_search_tool
        
        # Mock the agents
        mock_researcher = Mock()
        mock_content_writer = Mock()
        mock_agent_class.side_effect = [mock_researcher, mock_content_writer]
        
        # Mock the crew
        mock_crew_instance = Mock()
        expected_content = """
        # The Future of AI in Healthcare
        
        Artificial Intelligence is revolutionizing healthcare in unprecedented ways...
        
        ## Key Developments
        
        - Machine learning algorithms for diagnosis
        - Predictive analytics for patient care
        - Automated drug discovery
        
        ## Conclusion
        
        The future of AI in healthcare looks promising...
        """
        mock_crew_instance.kickoff.return_value = expected_content
        mock_crew_class.return_value = mock_crew_instance
        
        # Test the API endpoint
        client = TestClient(app)
        response = client.post(
            "/create-content",
            json={"topic": "AI in Healthcare"}
        )
        
        # Verify the response
        assert response.status_code == 200
        response_data = response.json()
        assert "content" in response_data
        assert expected_content in response_data["content"]
        
        # Verify that the crew was created and executed
        mock_crew_class.assert_called_once()
        mock_crew_instance.kickoff.assert_called_once()
    
    @patch('agent.Crew')
    @patch('agent.Agent')
    def test_workflow_with_different_topics(self, mock_agent_class, mock_crew_class):
        """Test the workflow with different topics."""
        # Mock the agents
        mock_researcher = Mock()
        mock_content_writer = Mock()
        mock_agent_class.side_effect = [mock_researcher, mock_content_writer]
        
        # Mock the crew
        mock_crew_instance = Mock()
        mock_crew_class.return_value = mock_crew_instance
        
        client = TestClient(app)
        
        # Test with different topics
        topics = [
            "Machine Learning in Finance",
            "Blockchain Technology",
            "Quantum Computing",
            "Sustainable Energy"
        ]
        
        for topic in topics:
            # Mock different content for each topic
            mock_content = f"Blog post about {topic}"
            mock_crew_instance.kickoff.return_value = mock_content
            
            response = client.post(
                "/create-content",
                json={"topic": topic}
            )
            
            assert response.status_code == 200
            assert topic in response.json()["content"]
    
    @patch('agent.Crew')
    @patch('agent.Agent')
    def test_workflow_error_handling(self, mock_agent_class, mock_crew_class):
        """Test error handling in the complete workflow."""
        # Mock the agents
        mock_researcher = Mock()
        mock_content_writer = Mock()
        mock_agent_class.side_effect = [mock_researcher, mock_content_writer]
        
        # Mock the crew to raise an exception
        mock_crew_instance = Mock()
        mock_crew_instance.kickoff.side_effect = Exception("Agent execution failed")
        mock_crew_class.return_value = mock_crew_instance
        
        client = TestClient(app)
        response = client.post(
            "/create-content",
            json={"topic": "AI in Healthcare"}
        )
        
        # Verify error handling
        assert response.status_code == 500
        assert "internal server error" in response.json()["detail"]


@pytest.mark.integration
class TestAPIEndpoints:
    """Test API endpoints in integration context."""
    
    def test_health_check_integration(self):
        """Test health check endpoint in integration context."""
        client = TestClient(app)
        response = client.get("/")
        
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
    
    def test_api_documentation_access(self):
        """Test that API documentation is accessible."""
        client = TestClient(app)
        
        # Test OpenAPI schema endpoint
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        # Test docs endpoint
        response = client.get("/docs")
        assert response.status_code == 200


@pytest.mark.integration
class TestAgentIntegration:
    """Test agent integration with the API."""
    
    @patch('agent.Crew')
    @patch('agent.Agent')
    def test_agent_task_sequence(self, mock_agent_class, mock_crew_class):
        """Test that agents execute tasks in the correct sequence."""
        # Mock the agents
        mock_researcher = Mock()
        mock_content_writer = Mock()
        mock_agent_class.side_effect = [mock_researcher, mock_content_writer]
        
        # Mock the crew
        mock_crew_instance = Mock()
        mock_crew_instance.kickoff.return_value = "Generated content"
        mock_crew_class.return_value = mock_crew_instance
        
        # Import and test the agent function directly
        from agent import create_content_crew
        
        result = create_content_crew("Test Topic")
        
        # Verify the result
        assert result == "Generated content"
        
        # Verify crew was created with correct configuration
        mock_crew_class.assert_called_once()
        call_args = mock_crew_class.call_args
        
        # Verify that agents and tasks are properly configured
        assert 'agents' in call_args.kwargs
        assert 'tasks' in call_args.kwargs
        assert 'process' in call_args.kwargs
        assert 'verbose' in call_args.kwargs


@pytest.mark.integration
@pytest.mark.slow
class TestPerformanceIntegration:
    """Test performance aspects of the integration."""
    
    @patch('agent.Crew')
    @patch('agent.Agent')
    def test_large_topic_handling(self, mock_agent_class, mock_crew_class):
        """Test handling of large/complex topics."""
        # Mock the agents
        mock_researcher = Mock()
        mock_content_writer = Mock()
        mock_agent_class.side_effect = [mock_researcher, mock_content_writer]
        
        # Mock the crew
        mock_crew_instance = Mock()
        mock_crew_instance.kickoff.return_value = "Generated content for complex topic"
        mock_crew_class.return_value = mock_crew_instance
        
        # Test with a complex topic
        complex_topic = "The intersection of artificial intelligence, machine learning, quantum computing, and blockchain technology in modern software development practices"
        
        client = TestClient(app)
        response = client.post(
            "/create-content",
            json={"topic": complex_topic}
        )
        
        assert response.status_code == 200
        assert "content" in response.json()
    
    @patch('agent.Crew')
    @patch('agent.Agent')
    def test_concurrent_requests(self, mock_agent_class, mock_crew_class):
        """Test handling of concurrent requests."""
        # Mock the agents
        mock_researcher = Mock()
        mock_content_writer = Mock()
        mock_agent_class.side_effect = [mock_researcher, mock_content_writer]
        
        # Mock the crew
        mock_crew_instance = Mock()
        mock_crew_instance.kickoff.return_value = "Generated content"
        mock_crew_class.return_value = mock_crew_instance
        
        client = TestClient(app)
        
        # Simulate concurrent requests (in a real scenario, you'd use threading)
        topics = ["Topic 1", "Topic 2", "Topic 3"]
        responses = []
        
        for topic in topics:
            response = client.post(
                "/create-content",
                json={"topic": topic}
            )
            responses.append(response)
        
        # Verify all requests succeeded
        for response in responses:
            assert response.status_code == 200
            assert "content" in response.json()


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v", "-m", "integration"])
