"""
Tests for the Streamlit chat interface.
"""
import pytest
from unittest.mock import MagicMock, patch
from src.streamlit import init_chat
from langchain_core.messages import AIMessage, HumanMessage

class MockSessionState:
    """Mock class for Streamlit's session state."""
    def __init__(self):
        self._dict = {}
    
    def __setattr__(self, name, value):
        if name == '_dict':
            super().__setattr__(name, value)
        else:
            self._dict[name] = value
    
    def __getattr__(self, name):
        if name not in self._dict:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        return self._dict[name]
    
    def __contains__(self, key):
        return key in self._dict

@pytest.fixture
def mock_streamlit():
    """Mock streamlit session state and functions."""
    with patch('src.streamlit.st') as mock_st:
        # Create a mock session state that behaves like Streamlit's
        mock_st.session_state = MockSessionState()
        yield mock_st

@pytest.fixture
def mock_chatllm():
    """Mock ChatOpenAI instance."""
    with patch('src.streamlit.ChatOpenAI') as mock_llm:
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = AIMessage(content="Test response")
        mock_llm.return_value = mock_instance
        yield mock_llm

def test_init_chat_creates_session_state(mock_streamlit, mock_chatllm):
    """Test that init_chat properly initializes session state."""
    init_chat()
    
    # Check that messages list was created
    assert "messages" in mock_streamlit.session_state
    assert isinstance(mock_streamlit.session_state.messages, list)
    assert len(mock_streamlit.session_state.messages) == 0
    
    # Check that LLM was initialized
    assert "llm" in mock_streamlit.session_state
    assert mock_chatllm.called

def test_init_chat_preserves_existing_messages(mock_streamlit, mock_chatllm):
    """Test that init_chat doesn't override existing messages."""
    # Setup existing messages
    existing_messages = [
        HumanMessage(content="Hello"),
        AIMessage(content="Hi there")
    ]
    mock_streamlit.session_state.messages = existing_messages
    
    init_chat()
    
    # Check that messages were preserved
    assert mock_streamlit.session_state.messages == existing_messages

def test_init_chat_preserves_existing_llm(mock_streamlit, mock_chatllm):
    """Test that init_chat doesn't recreate existing LLM."""
    # Setup existing LLM
    mock_existing_llm = MagicMock()
    mock_streamlit.session_state.llm = mock_existing_llm
    
    init_chat()
    
    # Check that LLM was preserved
    assert mock_streamlit.session_state.llm == mock_existing_llm
    # Check that new LLM was not created
    assert not mock_chatllm.called 