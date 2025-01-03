"""
LangChain agent implementation using DeepSeek LLM for executing bash commands.
"""
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.tools import ShellTool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.callbacks.base import BaseCallbackHandler

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

class TerminalAgent:
    """Agent class for executing bash commands using LangChain and DeepSeek."""
    
    def __init__(self, api_key: str):
        """
        Initialize the Terminal Agent.
        
        Args:
            api_key (str): DeepSeek API key
        """
        # Initialize the LLM
        self.llm = ChatOpenAI(
            model="deepseek-chat",
            api_key=api_key,
            base_url='https://api.deepseek.com/v1',
            streaming=True
        )
        
        # Create tools
        self.shell_tool = ShellTool()
        self.tools = [self.shell_tool]
        
        # Create prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant that can execute bash commands in a Linux environment. "
             "Always explain what you're doing before executing commands. "
             "Be careful with destructive commands and ask for confirmation when needed."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
    
    def execute(self, command: str, chat_history: List[BaseMessage], stream_handler: StreamHandler) -> None:
        """
        Execute a command through the agent.
        
        Args:
            command (str): The command or natural language request
            chat_history (List[BaseMessage]): The chat history
            stream_handler (StreamHandler): Handler for streaming tokens
        """
        # Update LLM with stream handler
        self.llm.callbacks = [stream_handler]
        
        # Create agent with updated LLM
        agent = create_openai_tools_agent(self.llm, self.tools, self.prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True
        )
        
        # Execute command
        agent_executor.invoke({
            "input": command,
            "chat_history": chat_history
        })


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY")
    agent = TerminalAgent(api_key=api_key)
    response = agent.execute("ls -l", [], StreamHandler(container=None))
    print(response)