from typing import Dict, Any, Optional
from .base_agent import BaseAgent

class ReentrancyAgent(BaseAgent):
    """
    Specialized agent for detecting reentrancy vulnerabilities.
    """

    def __init__(self, llm_config: Optional[Dict[str, Any]] = None):
        super().__init__(name="ReentrancyAgent", llm_config=llm_config)
        self.prompt = """
You are an expert in smart contract security, focusing on reentrancy vulnerabilities.
Analyze the Solidity code you will receive and look for:

1. Use of `call.value()()`, `.transfer()`, or `.send()` without reentrancy guards.
2. State changes that happen AFTER external calls.
3. Missing mutex or lock mechanisms (e.g., OpenZeppelin's ReentrancyGuard).
4. Cross-function reentrancy possibilities.

Provide a concise report of any findings with line references if possible,
as well as recommended improvements or mitigations.
"""