"""
LangChain agent implementation using DeepSeek LLM for executing bash commands.
"""
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.tools import ShellTool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

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
        
        # Create agent
        agent = create_openai_tools_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True
        )
    
    def execute(self, command: str, chat_history: List[BaseMessage]) -> Dict[str, Any]:
        """
        Execute a command through the agent.
        
        Args:
            command (str): The command or natural language request
            chat_history (List[BaseMessage]): The chat history
            
        Returns:
            Dict[str, Any]: The agent's response containing the output
        """
        return self.agent_executor.invoke({
            "input": command,
            "chat_history": chat_history
        }) 


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY")
    agent = TerminalAgent(api_key=api_key)
    response = agent.execute("ls -l", [])
    print(response)