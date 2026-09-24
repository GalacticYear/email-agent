import os
import json

def load_persistent_memory():
    """Reads saved user preferences across system restarts."""
    script_directory = os.path.dirname(os.path.abspath(__file__))
    memory_path = os.path.join(script_directory, "memory.json")
    
    if os.path.exists(memory_path):
        with open(memory_path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}