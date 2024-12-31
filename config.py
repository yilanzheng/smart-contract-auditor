import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

# LLM Provider Configurations
LLM_CONFIGS = {
    "openai": {
        "api_key_env": "OPENAI_API_KEY",
        "models": {
            "default": "gpt-4o",
            "available": ["gpt-4o", "gpt-4o-mini"]
        }
    },
    "anthropic": {
        "api_key_env": "ANTHROPIC_API_KEY",
        "models": {
            "default": "claude-3-5-sonnet-20241022",
            "available": [
                "claude-3-5-sonnet-20241022",
                "claude-3-opus-20240229",
                "claude-3-haiku-20240229"
            ]
        }
    }
}

# Default settings for all LLM configurations
DEFAULT_SETTINGS = {
    "timeout": 600,
    "temperature": 0,
    "seed": 42,
    "max_tokens": 1000
}

def get_llm_config(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Get LLM configuration, merging provided config with defaults.
    
    Args:
        config: Partial configuration dictionary. Can contain:
               - provider: LLM provider name
               - model: Model name (optional)
               - Any other settings to override defaults
    
    Returns:
        Complete configuration dictionary
    """
    # Start with default provider if none specified
    provider = (config or {}).get("provider", "anthropic")
    
    if provider not in LLM_CONFIGS:
        raise ValueError(f"Unsupported provider: {provider}")
        
    provider_config = LLM_CONFIGS[provider]
    api_key = os.getenv(provider_config["api_key_env"])
    
    if not api_key:
        raise ValueError(f"{provider_config['api_key_env']} not found")
    
    # Build base config with defaults
    base_config = {
        "provider": provider,
        "model": provider_config["models"]["default"],
        "api_key": api_key,
        **DEFAULT_SETTINGS
    }
    
    # Override with any provided config values
    if config:
        # Verify model if provided
        if "model" in config and config["model"] not in provider_config["models"]["available"]:
            raise ValueError(f"Invalid {provider} model: {config['model']}")
        
        base_config.update(config)
    
    return {"config_list": [base_config]}

# Initialize default configuration
DEFAULT_LLM_CONFIG = get_llm_config()

