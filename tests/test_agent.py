"""
Unit tests for the TerminalAgent class.
"""
import pytest
from unittest.mock import Mock, patch
import os
from dotenv import load_dotenv
from src.agent import TerminalAgent, StreamHandler
from langchain_core.messages import AIMessage, HumanMessage

# Load environment variables
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Constants
INTEGRATION_TIMEOUT = 30  # 30 seconds timeout for integration tests

@pytest.fixture
def terminal_agent():
    """Fixture to create a TerminalAgent instance with real API key."""
    return TerminalAgent(api_key=DEEPSEEK_API_KEY)

@pytest.fixture
def stream_handler():
    """Fixture to create a StreamHandler instance with a mock container."""
    mock_container = Mock()
    return StreamHandler(container=mock_container)

def test_terminal_agent_initialization(terminal_agent):
    """Test TerminalAgent initialization."""
    assert terminal_agent.llm is not None
    assert terminal_agent.shell_tool is not None
    assert len(terminal_agent.tools) == 1
    assert terminal_agent.prompt is not None
    assert terminal_agent.llm.model_name == "deepseek-chat"

def test_stream_handler():
    """Test StreamHandler token handling."""
    mock_container = Mock()
    handler = StreamHandler(container=mock_container, initial_text="Initial ")
    
    handler.on_llm_new_token("test", **{})
    assert handler.text == "Initial test"
    mock_container.markdown.assert_called_with("Initial test")

def test_stream_handler_multiple_tokens():
    """Test StreamHandler with multiple tokens."""
    mock_container = Mock()
    handler = StreamHandler(container=mock_container)
    
    tokens = ["Hello", " ", "World", "!"]
    expected_text = ""
    for token in tokens:
        handler.on_llm_new_token(token, **{})
        expected_text += token
        mock_container.markdown.assert_called_with(expected_text)

def test_stream_handler_empty():
    """Test StreamHandler with empty token."""
    mock_container = Mock()
    handler = StreamHandler(container=mock_container)
    
    handler.on_llm_new_token("", **{})
    assert handler.text == ""
    mock_container.markdown.assert_called_with("")

def test_terminal_agent_system_prompt(terminal_agent):
    """Test system prompt generation."""
    system_prompt = terminal_agent.get_system_prompt()
    assert isinstance(system_prompt, tuple)
    assert system_prompt[0] == "system"
    assert "Ubuntu" in system_prompt[1]
    assert "bash tool" in system_prompt[1]

@pytest.mark.timeout(INTEGRATION_TIMEOUT)
@pytest.mark.integration
def test_agent_execute_simple_command(terminal_agent, stream_handler, capsys):
    """Test executing a simple command."""
    mock_chat_history = []
    mock_command = "echo 'test output'"
    
    terminal_agent.execute(mock_command, mock_chat_history, stream_handler)
    
    captured = capsys.readouterr()
    assert "test output" in captured.out

@pytest.mark.timeout(INTEGRATION_TIMEOUT)
@pytest.mark.integration
def test_agent_execute_with_chat_history(terminal_agent, stream_handler, capsys):
    """Test executing command with chat history."""
    chat_history = [
        HumanMessage(content="What is the current directory?"),
        AIMessage(content="I'll help you find that out using the pwd command.")
    ]
    command = "pwd"
    
    terminal_agent.execute(command, chat_history, stream_handler)
    
    captured = capsys.readouterr()
    assert os.getcwd() in captured.out

@pytest.mark.timeout(INTEGRATION_TIMEOUT)
@pytest.mark.integration
def test_agent_execute_complex_command(terminal_agent, stream_handler, capsys):
    """Test executing a more complex command with pipes."""
    command = "ls -la | grep test"
    
    terminal_agent.execute(command, [], stream_handler)
    
    captured = capsys.readouterr()
    assert "test" in captured.out.lower()  # Should find our test directory

@pytest.mark.timeout(INTEGRATION_TIMEOUT)
@pytest.mark.integration
def test_agent_execute_invalid_command(terminal_agent, stream_handler, capsys):
    """Test executing an invalid command."""
    command = "invalid_command_that_does_not_exist"
    
    # Should not raise an exception but show error in output
    terminal_agent.execute(command, [], stream_handler)
    
    captured = capsys.readouterr()
    assert "command not found" in captured.out.lower() or "not found" in captured.out.lower()

@pytest.mark.timeout(INTEGRATION_TIMEOUT)
@pytest.mark.integration
def test_agent_execute_environment_command(terminal_agent, stream_handler, capsys):
    """Test executing a command that uses environment variables."""
    command = "echo $HOME"
    
    terminal_agent.execute(command, [], stream_handler)
    
    captured = capsys.readouterr()
    assert os.environ.get("HOME", "") in captured.out 