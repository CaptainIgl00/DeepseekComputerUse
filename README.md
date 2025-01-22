# DeepSeek Computer Use Demo

[![Tests](https://github.com/CaptainIgl00/DeepseekComputerUse/actions/workflows/test.yml/badge.svg)](https://github.com/CaptainIgl00/DeepseekComputerUse/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/CaptainIgl00/DeepseekComputerUse/branch/main/graph/badge.svg)](https://codecov.io/gh/CaptainIgl00/DeepseekComputerUse)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

A containerized application that combines a LangChain-powered terminal assistant with a virtual desktop environment, accessible through a web browser. The assistant uses the DeepSeek LLM to understand and execute bash commands in a controlled Ubuntu environment. This project is highly inspired by the Anthropic Computer Use Demo [https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo).

## Features

- 🤖 AI-powered terminal assistant using DeepSeek LLM
- 🖥️ Virtual Ubuntu desktop environment accessible via browser
- 🔒 Secure containerized execution environment
- 🌐 Web-based VNC access through noVNC
- 🖱️ Pre-installed desktop applications (Firefox, LibreOffice, etc.)
- 💻 Streamlit-based chat interface
- 🧪 Comprehensive test suite with 80%+ coverage
- 📊 Continuous Integration with GitHub Actions
- 🔍 Code quality checks with pre-commit hooks

## Prerequisites

- Docker and Docker Compose
- A DeepSeek API key
- Python 3.12+ (for development)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/CaptainIgl00/DeepseekComputerUse.git
cd DeepseekComputerUse
```

2. Create a `.env` file with your DeepSeek API key:
```bash
DEEPSEEK_API_KEY=your_api_key_here
```

3. Build and start the container:
```bash
docker-compose up --build
```

## Development Setup

1. Install development dependencies:
```bash
pip install -r requirements.txt
pip install pytest pytest-cov pytest-timeout pytest-mock pre-commit
```

2. Install pre-commit hooks:
```bash
pre-commit install
```

3. Run tests:
```bash
# Run unit tests
pytest -v -m "not integration"

# Run integration tests
pytest -v -m "integration"

# Run all tests with coverage
pytest -v --cov=src
```

## Accessing the Application

Once the container is running, you can access:
- Terminal assistant: http://localhost:8080
- Virtual desktop (noVNC): http://localhost:6080
- Streamlit interface: http://localhost:8501

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Run pre-commit hooks (`pre-commit run --all-files`)
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

