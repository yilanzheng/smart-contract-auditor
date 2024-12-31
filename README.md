# Smart Contract Security Analyzer

An automated smart contract security analysis tool that leverages multiple specialized agents to perform comprehensive security audits of Solidity smart contracts.

## Features

- Multi-agent architecture for specialized security analysis
- Comprehensive vulnerability detection across multiple domains:
  - Reentrancy vulnerabilities
  - Access control issues
  - Business logic flaws
  - Gas optimization opportunities
  - Integer overflow/underflow
- Severity-based issue prioritization
- Actionable recommendations for fixes
- Support for multiple LLM providers (OpenAI and Anthropic)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/smart-contract-analyzer.git
cd smart-contract-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
```

## Usage

Run the analyzer on a Solidity smart contract:
```bash
python main.py path/to/your/contract.sol
```

To save the report to a file:

```bash
python main.py path/to/your/contract.sol --output report.txt
```

## Configuration

The tool supports both Anthropic and OpenAI models. Default configuration can be modified in `config.py`:

- Default provider: Anthropic Claude
- Available models:
  - claude-3-5-sonnet-20241022
  - claude-3-opus-20240229
  - claude-3-haiku-20240229
  - gpt-4o
  - gpt-4o-mini

## Project Structure

```
├── agents/
│   ├── __init__.py
│   ├── coordinator.py
│   ├── base_agent.py
│   ├── access_control_agent.py
│   ├── business_logic_agent.py
│   ├── gas_agent.py
│   ├── overflow_agent.py
│   └── reentrancy_agent.py
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Disclaimer

This tool is provided as-is and should not be the only security measure used for smart contract auditing. Always perform thorough manual reviews and testing before deploying smart contracts to production.