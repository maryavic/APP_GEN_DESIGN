import os

def load_api_key():
    """
    Load API key from an environment variable or a configuration file.
    """
    return os.getenv("STABILITY_API_KEY")  # Or load from a config file
