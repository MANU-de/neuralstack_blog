# Content Creator API - Testing Guide

This document provides comprehensive information about the test suite for the Content Creator API.

## Test Structure

The test suite is organized into several modules:

- **`test_main.py`** - Unit tests for FastAPI endpoints and main application logic
- **`test_agent.py`** - Unit tests for CrewAI agent functionality
- **`test_integration.py`** - Integration tests for complete workflows
- **`conftest.py`** - Pytest configuration and shared fixtures
- **`pytest.ini`** - Pytest configuration file
- **`run_tests.py`** - Test runner script with various options

## Test Categories

### Unit Tests
- **API Endpoints**: Test FastAPI endpoints with various scenarios
- **Agent Functions**: Test CrewAI agent creation and execution
- **Error Handling**: Test error scenarios and exception handling
- **Validation**: Test input validation and data models

### Integration Tests
- **Complete Workflow**: Test the full process from API request to content generation
- **Agent Integration**: Test agent interaction with the API
- **Performance**: Test handling of large topics and concurrent requests

## Running Tests

### Prerequisites

1. Install test dependencies:
```bash
pip install -r requirements-test.txt
```

### Basic Test Execution

```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run specific test file
python -m pytest test_main.py

# Run specific test class
python -m pytest test_main.py::TestFastAPIEndpoints

# Run specific test method
python -m pytest test_main.py::TestFastAPIEndpoints::test_health_check_endpoint
```

### Using the Test Runner Script

```bash
# Run all tests with coverage
python run_tests.py --coverage --verbose

# Run only unit tests
python run_tests.py --unit

# Run only integration tests
python run_tests.py --integration

# Run tests with HTML report
python run_tests.py --html --coverage

# Skip slow tests
python run_tests.py --fast

# Install dependencies and run tests
python run_tests.py --install-deps --coverage
```

### Test Markers

Tests are organized using pytest markers:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow-running tests
- `@pytest.mark.api` - API endpoint tests
- `@pytest.mark.agent` - Agent functionality tests

Run tests by marker:
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

## Test Coverage

The test suite provides comprehensive coverage of:

### API Endpoints (test_main.py)
- ✅ Health check endpoint
- ✅ Content creation endpoint (success/failure scenarios)
- ✅ Input validation
- ✅ Error handling
- ✅ Logging functionality

### Agent Functionality (test_agent.py)
- ✅ Agent initialization with/without search tools
- ✅ Crew creation and configuration
- ✅ Task definition and execution
- ✅ Error handling in agent execution
- ✅ Environment variable validation

### Integration Tests (test_integration.py)
- ✅ Complete workflow from API to agent
- ✅ Multiple topic handling
- ✅ Error handling in complete workflow
- ✅ Performance testing
- ✅ Concurrent request handling

## Mocking Strategy

The tests use comprehensive mocking to isolate components:

### FastAPI Testing
- Uses `TestClient` for API endpoint testing
- Mocks external dependencies (CrewAI agents)
- Simulates various response scenarios

### Agent Testing
- Mocks CrewAI `Agent` and `Crew` classes
- Mocks search tools and external APIs
- Simulates different execution outcomes

### Environment Testing
- Mocks environment variables
- Tests with/without API keys
- Simulates different configuration scenarios

## Test Data

### Sample Requests
```python
# Valid content request
{
    "topic": "AI in Healthcare"
}

# Complex topic
{
    "topic": "The intersection of artificial intelligence, machine learning, quantum computing, and blockchain technology"
}
```

### Sample Responses
```python
# Successful content generation
{
    "content": "Generated blog post content..."
}

# Error responses
{
    "detail": "Content creation failed, received no output from the agent."
}
```

## Continuous Integration

The test suite is designed to work with CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          pip install -r requirements-test.txt
      - name: Run tests
        run: |
          python run_tests.py --coverage --html
```

## Debugging Tests

### Running Tests in Debug Mode
```bash
# Run with maximum verbosity
pytest -vvv --tb=long

# Run with pdb debugger
pytest --pdb

# Run specific test with debug output
pytest test_main.py::TestFastAPIEndpoints::test_create_content_success -vvv
```

### Common Issues

1. **Import Errors**: Ensure the project root is in Python path
2. **Mock Issues**: Check that mocks are properly configured
3. **Environment Variables**: Ensure test environment is properly set up

## Test Reports

The test suite generates several types of reports:

### Coverage Report
```bash
pytest --cov=. --cov-report=html
# Generates: htmlcov/index.html
```

### HTML Test Report
```bash
pytest --html=test_report.html --self-contained-html
# Generates: test_report.html
```

### JSON Report
```bash
pytest --json-report --json-report-file=test_results.json
# Generates: test_results.json
```

## Best Practices

1. **Isolation**: Each test is independent and can run in any order
2. **Mocking**: External dependencies are properly mocked
3. **Coverage**: Aim for high test coverage of critical paths
4. **Performance**: Include performance tests for critical workflows
5. **Documentation**: Tests serve as living documentation

## Adding New Tests

When adding new functionality:

1. **Unit Tests**: Add tests for individual functions/methods
2. **Integration Tests**: Add tests for complete workflows
3. **Error Cases**: Test error scenarios and edge cases
4. **Performance**: Add performance tests for critical paths

### Example Test Structure
```python
class TestNewFeature:
    """Test new feature functionality."""
    
    def test_feature_success(self):
        """Test successful feature execution."""
        # Arrange
        # Act
        # Assert
    
    def test_feature_error(self):
        """Test feature error handling."""
        # Arrange
        # Act
        # Assert
```

## Troubleshooting

### Common Test Failures

1. **Mock Not Called**: Check mock configuration and call assertions
2. **Import Errors**: Verify Python path and module structure
3. **Environment Issues**: Check environment variable setup
4. **Timeout Issues**: Increase timeout for slow tests

### Getting Help

- Check test output for detailed error messages
- Use `pytest --tb=long` for full traceback
- Run individual tests to isolate issues
- Check mock configurations and assertions
