from typing import Dict, Any, Optional
from .base_agent import BaseAgent

class GasAgent(BaseAgent):
    """
    Specialized agent for identifying gas optimization opportunities.
    """

    def __init__(self, llm_config: Optional[Dict[str, Any]] = None):
        super().__init__(name="GasAgent", llm_config=llm_config)
        self.prompt = """
You are a Solidity performance and optimization expert.
Review the contract code for potential gas inefficiencies:

1. Unnecessarily large loops or repeated storage writes.
2. Suboptimal data structures (e.g., arrays when mappings could be more efficient).
3. Functions that combine multiple state changes that can be split to reduce gas.
4. Overuse of expensive opcodes or repeated computations.

Provide suggestions to reduce gas usage, referencing code segments when possible.
"""