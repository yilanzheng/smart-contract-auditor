from typing import Dict, Any, Optional

import openai
import anthropic
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

from config import get_llm_config, DEFAULT_LLM_CONFIG

class BaseAgent:
    """
    A base agent that encapsulates shared logic for specialized agents
    without relying on autogen.
    """
    def __init__(self, name: str, llm_config: Optional[Dict[str, Any]] = None):
        """
        Initialize the agent with a name and optional LLM configuration.
        
        Args:
            name: Agent name
            llm_config: Can be either:
                       - None (uses default configuration)
                       - A complete config dict
                       - A partial config dict (e.g., {"provider": "anthropic"})
        """
        self.name = name
        self.llm_config = get_llm_config(llm_config) if llm_config else DEFAULT_LLM_CONFIG
        self.prompt = ""  # to be set by subclasses
        
        # Initialize client based on provider
        self._init_client()
        
    def _init_client(self):
        """Initialize the appropriate LLM client based on provider configuration."""
        config = self.llm_config["config_list"][0]
        provider = config["provider"]
        api_key = config["api_key"]
        
        if provider == "openai":
            openai.api_key = api_key
            self.client = openai.chat.completions
        elif provider == "anthropic":
            self.client = Anthropic(api_key=api_key)
        else:
            raise ValueError(f"Unknown provider '{provider}'. Must be 'openai' or 'anthropic'.")

    def analyze(self, contract_code: str) -> str:
        return self._call_llm(system_message=self.prompt, user_message=contract_code)

    def _call_llm(self, system_message: str, user_message: str) -> str:
        """Call LLM with unified interface for both providers."""
        config = self.llm_config["config_list"][0]
        
        if config["provider"] == "openai":
            response = self.client.create(
                model=config["model"],
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                ],
                temperature=config["temperature"],
                max_tokens=config["max_tokens"],
            )
            return response.choices[0].message.content
            
        else:  # anthropic
            prompt = f"{HUMAN_PROMPT} System: {system_message}\n\nUser: {user_message}{AI_PROMPT}"
            response = self.client.messages.create(
                model=config["model"],
                max_tokens=config["max_tokens"],
                temperature=config["temperature"],
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text

