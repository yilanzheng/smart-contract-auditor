from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from .prompts import ANALYZER_PROMPT

class AnalyzerAgent(BaseAgent):
    """
    Specialized agent for identifying gas optimization opportunities.
    """

    def __init__(self, llm_config: Optional[Dict[str, Any]] = None):
        super().__init__(name="AnalyzerAgent", llm_config=llm_config)
        self.prompt = ANALYZER_PROMPT