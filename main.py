import autogen
from typing import List, Dict
import json
import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
from prompt import coordinator_prompt, static_analyzer_prompt, security_agent_prompt, business_logic_prompt, gas_optimizer_prompt

load_dotenv()
# Configure the LLM
config_list = [
    {
        "model": "gpt-4o-2024-08-06",
        "api_key": os.environ["OPENAI_API_KEY"],
    }
]

# Assistant configurations
assistant_config = {
    "cache_seed": 42,
    "temperature": 0.1,
    "config_list": config_list,
    "timeout": 120,
}

# Create the specialized agents

# Lead Auditor - Coordinates the audit process and compiles final report
coordinator = autogen.AssistantAgent(
    name="Coordinator",
    system_message=coordinator_prompt,
    llm_config=assistant_config
)

static_analyst = autogen.AssistantAgent(
    name="StaticAnalyst",
    system_message=static_analyzer_prompt,
    llm_config=assistant_config
)   

security_analyst = autogen.AssistantAgent(
    name="SecurityAnalyst",
    system_message=security_agent_prompt,
    llm_config=assistant_config
)

business_logic_analyst = autogen.AssistantAgent(
    name="BusinessLogicAnalyst",
    system_message=business_logic_prompt,
    llm_config=assistant_config
)

gas_optimizer = autogen.AssistantAgent(
    name="GasOptimizer",
    system_message=gas_optimizer_prompt,
    llm_config=assistant_config
)

# Human proxy for interaction
user_proxy = autogen.ConversableAgent(
    name="User",
    human_input_mode="NEVER",
    system_message="""You are a proxy for the user who wants to audit their smart contract.
    Provide the contract code and requirements when asked."""
)

class SmartContractAuditSystem:
    def __init__(self):
        self.agents = {
            "coordinator": coordinator,
            "static_analyst": static_analyst,
            "security_analyst": security_analyst,
            "business_logic_analyst": business_logic_analyst,
            "gas_optimizer": gas_optimizer,
        }
        
        # Create group chat for all agents
        self.group_chat = autogen.GroupChat(
            agents=list(self.agents.values()),
            messages=[],
            max_round=12,
        )
        
        # Create manager for the group chat
        self.manager = autogen.GroupChatManager(
            groupchat=self.group_chat,
            llm_config={"config_list": config_list}
        )

    def audit_contract(self, contract_code):
        
        # Start the group chat
        chat_result = user_proxy.initiate_chat(
            self.manager,
            message=f"""
        Analyze the following smart contract code and provide a comprehensive audit report.
        {contract_code}
        """,
        summary_method="reflection_with_llm",
        )

        return chat_result.summary


def read_contract(file_path: str) -> str:
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading contract file: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Smart Contract Auditor')
    parser.add_argument('contract_path', type=str, help='Path to the Solidity contract file')
    parser.add_argument('--output', '-o', type=str, help='Optional path for saving the report as JSON')
    
    args = parser.parse_args()
    
    # Read contract
    contract_code = read_contract(args.contract_path)
    if not contract_code:
        return
    
    # Run the audit
    print("Starting contract audit...")
    audit_system = SmartContractAuditSystem()
    report = audit_system.audit_contract(contract_code)
    
    # Handle output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report)
    else:
        print("\n=== FINAL AUDIT REPORT ===\n")
        print(report)

    
    print("\nAudit complete!")

if __name__ == "__main__":
    main()