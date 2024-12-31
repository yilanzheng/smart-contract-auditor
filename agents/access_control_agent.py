from typing import Dict, Any, Optional
from .base_agent import BaseAgent

class AccessControlAgent(BaseAgent):
    """
    Specialized agent for detecting access control vulnerabilities and authorization issues.
    """

    def __init__(self, llm_config: Optional[Dict[str, Any]] = None):
        super().__init__(name="AccessControlAgent", llm_config=llm_config)
        self.prompt = """
You are an expert in access control and authorization for Solidity smart contracts.
Analyze the provided code for:

1. Missing or incorrect modifiers (e.g., `onlyOwner`, `onlyRole`).
2. Privilege escalation (e.g., can a user obtain admin rights?).
3. Insecure role management or insufficient checks on critical functions.
4. Lack of separation between read-only and administrative functions.

Detail any vulnerabilities found, referencing lines or function names.
Recommend best practices for safe role-based access.
"""