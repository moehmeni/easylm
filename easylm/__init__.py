from .answer import ask


def default(configs: dict):
    """Configures the default settings for the library."""
    from .config import DEFAULT_SETTINGS

    for key, value in configs.items():
        DEFAULT_SETTINGS[key] = value


def add_provider(name: str, endpoint: str, key: str):
    """Adds a new provider to the library."""
    from .config import PROVIDERS_MAP

    PROVIDERS_MAP[name] = {"endpoint": endpoint, "key": key}
