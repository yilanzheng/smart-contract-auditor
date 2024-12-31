from typing import Dict, Any, Optional
from .base_agent import BaseAgent

class OverflowAgent(BaseAgent):
    """
    Specialized agent for detecting integer overflow and underflow issues.
    """

    def __init__(self, llm_config: Optional[Dict[str, Any]] = None):
        super().__init__(name="OverflowAgent", llm_config=llm_config)
        self.prompt = """
You are an expert in detecting integer overflow and underflow issues in Solidity.
Look for:

1. Arithmetic operations on user-controlled input without using SafeMath (pre-Solidity 0.8).
2. Potential overflow in loops or multiplication.
3. Mismatched integer types (e.g., uint8 vs uint256).
4. Any arithmetic that could exceed the maximum or minimum value of its data type.

Explain potential exploits and recommend secure handling, referencing code lines if possible.
"""