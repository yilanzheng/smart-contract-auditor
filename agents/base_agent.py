from typing import Dict, Any, Optional
from autogen import AssistantAgent
from config import DEFAULT_LLM_CONFIG

class BaseAgent:
    """
    A base agent that encapsulates shared logic for specialized agents.
    Each derived agent should define a self.prompt string and override
    the analyze() method if needed.
    """

    def __init__(self, name: str, llm_config: Optional[Dict[str, Any]] = None):
        
        """
        :param name: Name of the agent (e.g., "ReentrancyAgent").
        :param llm_config: Dict containing LLM credentials/configs 
                           (like model name, API key).
        """
        self.name = name
        self.llm_config = llm_config or DEFAULT_LLM_CONFIG
        self.prompt = ""  # to be set by subclasses
        self.agent = None

    def initialize_agent(self):
        """
        Construct the AssistantAgent from AutoGen if not already created.
        """
        if self.agent is None:
            self.agent = AssistantAgent(
                name=self.name,
                llm_config=self.llm_config,
                system_message=self.prompt
            )

    def analyze(self, contract_code: str) -> str:
        """
        Run the LLM-based analysis on the provided contract code.
        Subclasses may override self.prompt to include specialized instructions.

        :param contract_code: Solidity source code as a string.
        :return: Agent's response as a string.
        """
        self.initialize_agent()
        
        return self.agent.generate_reply(messages=[{"role": "user", "content": contract_code}])

