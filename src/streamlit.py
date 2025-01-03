"""
Streamlit chat interface with LangChain agent using DeepSeek LLM.
"""
import streamlit as st
from typing import List
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
import os
from agent import TerminalAgent

def init_chat() -> None:
    """Initialize chat session state if it doesn't exist."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "agent" not in st.session_state:
        load_dotenv()
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            st.error("Please set DEEPSEEK_API_KEY in your .env file")
            st.stop()
        st.session_state.agent = TerminalAgent(api_key=api_key)

def main() -> None:
    """Main Streamlit application."""
    st.title("🤖 Terminal Assistant")
    
    # Initialize chat
    init_chat()
    
    # Display chat messages
    for message in st.session_state.messages:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
    
    # Chat input
    if prompt := st.chat_input("What command would you like to execute?"):
        # Add user message to chat history
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.agent.execute(prompt, st.session_state.messages)
                st.markdown(response["output"])
                st.session_state.messages.append(AIMessage(content=response["output"]))
