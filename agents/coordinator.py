from typing import Dict, Any, Optional, List
from .base_agent import BaseAgent
from .gas_agent import GasAgent
from .access_control_agent import AccessControlAgent
from .business_logic_agent import BusinessLogicAgent
from .overflow_agent import OverflowAgent
from .reentrancy_agent import ReentrancyAgent

class CoordinatorAgent(BaseAgent):
    """
    Coordinator agent that orchestrates the analysis workflow and summarizes findings
    from all specialized security analysis agents.
    """

    def __init__(self, llm_config: Optional[Dict[str, Any]] = None):
        super().__init__(name="CoordinatorAgent", llm_config=llm_config)

        self.prompt = """
You are an expert smart contract security coordinator who synthesizes findings from specialized security agents.

When presented with security findings, you will create a comprehensive security report that:
1. Prioritizes critical vulnerabilities that require immediate attention
2. Groups related issues across different security domains (e.g., a reentrancy issue that also impacts gas costs)
3. Assigns severity levels (Critical, High, Medium, Low) based on potential impact
4. Provides specific, actionable recommendations for fixing each issue
5. Highlights any patterns or common themes in the vulnerabilities

Each finding in your report should include:
- Severity Level
- Related Security Domains
- Description of the Issue
- Potential Impact
- Recommended Fix
"""

        # Initialize specialized agents
        self.agents = {
            "Reentrancy": ReentrancyAgent(),
            "Access Control": AccessControlAgent(),
            "Business Logic": BusinessLogicAgent(),
            "Gas Optimization": GasAgent(),
            "Overflow": OverflowAgent()
        }
        
        # If custom llm_config is provided, update all agents
        if llm_config is not None:
            for agent in self.agents.values():
                agent.llm_config = llm_config

    def audit_contract(self, contract_code: str) -> str:
        """
        Coordinate analysis across all specialized agents and summarize findings.

        :param contract_code: Solidity source code as a string
        :return: Consolidated analysis report
        """
        # Collect findings from all specialized agents
        findings = {}
        for agent_name, agent in self.agents.items():
            findings[agent_name] = agent.analyze(contract_code)
        
        summary_prompt = self._create_summary_prompt(findings)
        return super().analyze(summary_prompt)

    def _create_summary_prompt(self, findings: Dict[str, str]) -> str:
        prompt = "Please analyze the following security findings and create a comprehensive report:\n\n"
        
        for agent_name, result in findings.items():
            prompt += f"=== {agent_name.upper()} ANALYSIS ===\n"
            prompt += f"{result}\n\n"
            
        return prompt