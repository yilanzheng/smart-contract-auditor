import autogen
from typing import List, Dict
import json
import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
from prompt import ENTRY_POINTS_PROMPT, ANALYZER_PROMPT, EXPLOIT_DESIGNER_PROMPT, EXPLOIT_VALIDATOR_PROMPT

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
# Entry Points Analyzer - Identifies potential entry points for attacks
entry_points_analyzer = autogen.AssistantAgent(
    name="EntryPointsAnalyzer",
    system_message=ENTRY_POINTS_PROMPT,
    llm_config=assistant_config
)

# Function Analyzer - Analyzes individual functions in detail
analyzer = autogen.AssistantAgent(
    name="Analyzer", 
    system_message=ANALYZER_PROMPT,
    llm_config=assistant_config
)

# Exploit Designer - Designs potential exploits
exploit_designer = autogen.AssistantAgent(
    name="ExploitDesigner",
    system_message=EXPLOIT_DESIGNER_PROMPT,
    llm_config=assistant_config
)

# Exploit Validator - Validates proposed exploits
exploit_validator = autogen.AssistantAgent(
    name="ExploitValidator",
    system_message=EXPLOIT_VALIDATOR_PROMPT,
    llm_config=assistant_config
)


reporter = autogen.AssistantAgent(
    "reporter",
    system_message="""
        You are a smart contract audit reporter. You will aggregate the findings from all other agents.
        Format the results into a clear and concise audit report.
        List all vulnerabilities, their severity, description, and potential remediation.
    """,
    llm_config=assistant_config
)

# Human proxy for interaction
user_proxy = autogen.ConversableAgent(
    name="User",
    human_input_mode="NEVER",
    system_message="""You are a proxy for the user who wants to audit their smart contract.
    Provide the contract code and requirements when asked."""
)

groupchat = autogen.GroupChat(agents=[user_proxy, entry_points_analyzer, analyzer, exploit_designer, exploit_validator, reporter], 
                              messages=[], 
                              max_round=10,
                              speaker_selection_method="round_robin")
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=assistant_config)

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
    user_proxy.initiate_chat(
        manager,
        message=f"""
        Analyze the following smart contract code and provide a comprehensive audit report.
        {contract_code}
        """
    )
    


    
    print("\nAudit complete!")

if __name__ == "__main__":
    main()