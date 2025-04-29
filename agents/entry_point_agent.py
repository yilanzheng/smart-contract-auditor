from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from .prompts import ENTRY_POINTS_PROMPT

class EntryPointAgent(BaseAgent):
    """
    Specialized agent for identifying gas optimization opportunities.
    """

    def __init__(self, llm_config: Optional[Dict[str, Any]] = None):
        super().__init__(name="EntryPointAgent", llm_config=llm_config)
        self.prompt = ENTRY_POINTS_PROMPT