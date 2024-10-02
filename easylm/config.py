import os
from typing import Dict, Any

DEFAULT_SETTINGS: Dict[str, Any] = {
    "model": "openai/gpt-3.5-turbo",
    "params": {
        "max_tokens": 100,
        "temperature": 1,
    },
}

PROVIDERS_MAP: Dict[str, Dict[str, str]] = {
    "openrouter": {
        "endpoint": "https://openrouter.ai/api/v1/chat/completions",
        "key": "OPENROUTER_API_KEY",
    },
    "openai": {
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "key": "OPENAI_API_KEY",
    },
    "ollama": {
        "endpoint": "",  # TODO: Add Ollama endpoint
        "key": "OLLAMA_API_KEY",
    },
}

def get_api_key(provider: str) -> str:
    key_name = PROVIDERS_MAP[provider]["key"]
    api_key = os.getenv(key_name)
    if not api_key:
        raise ValueError(f"Please set the {key_name} environment variable")
    return api_key
