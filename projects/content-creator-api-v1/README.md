# Content Creator API

A FastAPI-based application that uses CrewAI agents to generate blog posts on any given topic. The API leverages AI agents to research and write comprehensive, SEO-optimized content.

## Features

- 🤖 **AI-Powered Content Generation**: Uses CrewAI agents for intelligent content creation
- 🔍 **Research Capabilities**: Integrated web search for up-to-date information
- 📝 **SEO-Optimized Output**: Generates well-structured, engaging blog posts
- 🚀 **FastAPI Backend**: High-performance, async API with automatic documentation
- 🧪 **Comprehensive Testing**: Full test suite with unit and integration tests
- 📊 **Health Monitoring**: Built-in health check endpoints

## Architecture

The application consists of two main components:

1. **FastAPI Application** (`main.py`): Handles HTTP requests and responses
2. **CrewAI Agents** (`agent.py`): Manages AI agents for research and content creation

### Agent Workflow

1. **Research Agent**: Conducts comprehensive research on the given topic
2. **Content Writer Agent**: Transforms research into engaging blog posts
3. **Sequential Processing**: Tasks are executed in order for optimal results

## Installation

### Prerequisites

- Python 3.11+
- OpenAI API Key
- Serper API Key (optional, for web search)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd content-creator-api
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   SERPER_API_KEY=your_serper_api_key_here  # Optional
   ```

## Usage

### Running the Application

1. **Start the server**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/

### API Endpoints

#### Create Content
```http
POST /create-content
Content-Type: application/json

{
  "topic": "AI in Healthcare"
}
```

**Response**:
```json
{
  "content": "# AI in Healthcare\n\nArtificial Intelligence is revolutionizing healthcare..."
}
```

#### Health Check
```http
GET /
```

**Response**:
```json
{
  "status": "ok"
}
```

### Example Usage

```python
import requests

# Create content
response = requests.post(
    "http://localhost:8000/create-content",
    json={"topic": "The Future of Machine Learning"}
)

if response.status_code == 200:
    content = response.json()["content"]
    print(content)
else:
    print(f"Error: {response.json()}")
```

## Testing

The project includes a comprehensive test suite covering all functionality.

### Running Tests

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=. --cov-report=html

# Run specific test categories
python -m pytest -m unit
python -m pytest -m integration
```

### Test Structure

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Performance Tests**: Large topic and concurrent request handling

## Development

### Project Structure

```
content-creator-api/
├── main.py                 # FastAPI application
├── agent.py               # CrewAI agents and crew logic
├── test_main.py          # Unit tests for API endpoints
├── test_agent.py         # Unit tests for agent functionality
├── test_integration.py   # Integration tests
├── conftest.py           # Pytest configuration
├── run_tests.py          # Test runner script
├── requirements.txt      # Production dependencies
├── requirements-test.txt # Test dependencies
├── pytest.ini           # Pytest configuration
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

### Adding New Features

1. **Write Tests First**: Follow TDD principles
2. **Update Documentation**: Keep README and docstrings current
3. **Run Tests**: Ensure all tests pass
4. **Code Review**: Follow best practices

## Deployment

### Using ngrok for Development

1. **Start the application**:
   ```bash
   uvicorn main:app --reload
   ```

2. **In another terminal, start ngrok**:
   ```bash
   ngrok http 8000
   ```

3. **Use the ngrok URL** in your Google Apps Script or other integrations

### Production Deployment

For production deployment, consider:

- **Environment Variables**: Secure API key management
- **Process Management**: Use PM2 or similar
- **Load Balancing**: For high-traffic scenarios
- **Monitoring**: Health checks and logging
- **Security**: HTTPS, rate limiting, input validation

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions or issues:
1. Check the [documentation](TEST_README.md)
2. Review existing [issues](../../issues)
3. Create a new [issue](../../issues/new)

## Changelog

### v1.0.0
- Initial release
- FastAPI backend with CrewAI integration
- Comprehensive test suite
- API documentation
- Health check endpoints
