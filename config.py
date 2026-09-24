import os
from dotenv import load_dotenv

# Load variables safely from an external localized dot-env structure environment
load_dotenv()

# Centralized provider token configurations
API_KEY = os.getenv("MODEL_PROVIDER_API_KEY", "")
BASE_URL = os.getenv("MODEL_PROVIDER_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("MODEL_NAME", "qwen 2.5:3b")
MODEL_NAME = OLLAMA_MODEL

if not API_KEY and "localhost" not in BASE_URL:
    print("WARNING: No model provider API token discovered in system environment variables.")
