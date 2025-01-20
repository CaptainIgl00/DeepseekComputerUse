# DeepSeek Computer Use Demo

A containerized application that combines a LangChain-powered terminal assistant with a virtual desktop environment, accessible through a web browser. The assistant uses the DeepSeek LLM to understand and execute bash commands in a controlled Ubuntu environment. This project is highly inspired by the Anthropic Computer Use Demo [https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo).

## Features

- 🤖 AI-powered terminal assistant using DeepSeek LLM
- 🖥️ Virtual Ubuntu desktop environment accessible via browser
- 🔒 Secure containerized execution environment
- 🌐 Web-based VNC access through noVNC
- 🖱️ Pre-installed desktop applications (Firefox, LibreOffice, etc.)
- 💻 Streamlit-based chat interface

## Prerequisites

- Docker and Docker Compose
- A DeepSeek API key

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

## Accessing the Application

Once the container is running, you can access the terminal assistant at http://localhost:8501.

