from typing import Dict, Any, Optional, List
from .base_agent import BaseAgent
from .gas_agent import GasAgent
from .access_control_agent import AccessControlAgent
from .business_logic_agent import BusinessLogicAgent
from .overflow_agent import OverflowAgent
from .reentrancy_agent import ReentrancyAgent
from .entry_point_agent import EntryPointAgent
from .analyzer_agent import AnalyzerAgent
from .exploit_designer import ExploitDesignerAgent
from .exploit_validator import ExploitValidatorAgent

class CoordinatorAgent(BaseAgent):
    """
    Coordinator agent that orchestrates the analysis workflow and summarizes findings
    from all specialized security analysis agents.
    """

    def __init__(self, llm_config: Optional[Dict[str, Any]] = None):
        super().__init__(name="CoordinatorAgent", llm_config=llm_config)

        self.prompt = """
You are a smart contract audit reporter. You will aggregate the findings from all other agents.
        Format the results into a clear and concise audit report.
        List all vulnerabilities, their severity, description, and potential remediation.
"""

        # Initialize specialized agents
        self.agents = {
            "EntryPointAgent": EntryPointAgent(llm_config=llm_config),
            "AnalyzerAgent": AnalyzerAgent(llm_config=llm_config),
            "ExploitDesignerAgent": ExploitDesignerAgent(llm_config=llm_config),
            "ExploitValidatorAgent": ExploitValidatorAgent(llm_config=llm_config),
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
            print(f"Findings from {agent_name}: {findings[agent_name]}")


        # summary_prompt = self._create_summary_prompt(findings)
        # return super().analyze(summary_prompt)

    def _create_summary_prompt(self, findings: Dict[str, str]) -> str:
        prompt = "Please analyze the following security findings and create a comprehensive report:\n\n"
        
        for agent_name, result in findings.items():
            prompt += f"=== {agent_name.upper()} ANALYSIS ===\n"
            prompt += f"{result}\n\n"
            
        return prompt