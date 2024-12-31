from typing import Dict, Any, Optional
from .base_agent import BaseAgent

class BusinessLogicAgent(BaseAgent):
    """
    Specialized agent for detecting logical flaws in the overall business logic of the contract.
    """

    def __init__(self, llm_config: Optional[Dict[str, Any]] = None):
        super().__init__(name="BusinessLogicAgent", llm_config=llm_config)
        self.prompt = """
You are an expert in high-level business logic and functional correctness for Solidity smart contracts.
Analyze the contract for:

1. Logical flaws, such as missing checks, incorrect assumptions, or broken state transitions.
2. Potential front-running vulnerabilities (e.g., a user can manipulate state by seeing pending transactions).
3. Integration with external protocols or price oracles (are they validated?).
4. Consistency between function inputs and expected outputs or states.

Highlight any discovered issues and suggest how to fix or mitigate them.
"""