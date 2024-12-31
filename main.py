import argparse
from pathlib import Path
from agents.coordinator import CoordinatorAgent
from config import DEFAULT_LLM_CONFIG

def read_contract(file_path: str) -> str:
    """
    Read a smart contract file.
    
    :param file_path: Path to the Solidity file
    :return: Contract source code or None if file cannot be read
    """
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
    
    # Initialize coordinator with agents
    coordinator = CoordinatorAgent(DEFAULT_LLM_CONFIG)
    
    # Run the audit
    print("Starting contract audit...")
    report = coordinator.audit_contract(contract_code)
    
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
