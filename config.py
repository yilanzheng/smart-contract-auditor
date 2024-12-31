import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Provider-specific configurations
OPENAI_CONFIG = {
    "default_model": "gpt-4o",
    "available_models": ["gpt-4o", "gpt-4o-mini"]
}

ANTHROPIC_CONFIG = {
    "default_model": "claude-3-5-sonnet",
    "available_models": ["claude-3-5-sonnet", "claude-3-opus", "claude-3-haiku"]
}

def get_config_list(provider: str, model: str = None) -> List[Dict[str, Any]]:
    """
    Get configuration list for specified provider.
    If model is not specified, uses the provider's default model.
    """
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found")
            
        # Use provided model or fall back to default
        model_name = model or OPENAI_CONFIG["default_model"]
        if model_name not in OPENAI_CONFIG["available_models"]:
            raise ValueError(f"Invalid OpenAI model: {model_name}")
            
        return [{
            "model": model_name,
            "api_key": api_key,
            **LLM_CONFIG_DEFAULTS
        }]
        
    elif provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")
            
        # Use provided model or fall back to default
        model_name = model or ANTHROPIC_CONFIG["default_model"]
        if model_name not in ANTHROPIC_CONFIG["available_models"]:
            raise ValueError(f"Invalid Anthropic model: {model_name}")
            
        return [{
            "model": model_name,
            "api_key": api_key,
            **LLM_CONFIG_DEFAULTS
        }]
    else:
        raise ValueError(f"Unsupported provider: {provider}")

# Default configuration
LLM_CONFIG_DEFAULTS = {
    "timeout": 600,
    "temperature": 0,
    "seed": 42
}

# Initialize default configuration
DEFAULT_LLM_CONFIG = {
    **LLM_CONFIG_DEFAULTS,
    "config_list": get_config_list("openai")  # Using default provider
}

