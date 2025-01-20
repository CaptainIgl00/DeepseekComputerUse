"""
LangChain agent implementation using DeepSeek LLM for executing bash commands.
"""
from typing import List
import platform
from datetime import datetime
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
            self.get_system_prompt(),
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


    def get_system_prompt(self):
        return ("system", f"* You are utilising an Ubuntu virtual machine using {platform.machine()} architecture with internet access. "
                "* You can use the bash tool to execute commands and the str_replace_editor tool to edit files. "
                "* Using bash tool you can start GUI applications, but you need to set export DISPLAY=:1 and use a subshell. For example '(DISPLAY=:1 xterm &)'. Consider that the GUI apps always appear."
                "* When using bash tool with commands that are expected to output very large quantities of text, redirect into a tmp file. "
                f"* The current date is {datetime.today().strftime('%A, %B %-d, %Y')}.")