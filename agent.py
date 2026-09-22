import json
import urllib.request
import config

def call_llm(prompt: str) -> str:
    """Sends a string prompt to a local Ollama instance and returns the text response."""
    # 1. Prepare payload dictionary
    payload = {
        "model": config.OLLAMA_MODEL, 
        "prompt": prompt, 
        "stream": False
    }
    
    # 2. Convert dictionary to raw bytes
    data = json.dumps(payload).encode("utf-8")
    
    try:
        # 3. Create HTTP Request configuration
        req = urllib.request.Request(
            config.OLLAMA_URL, 
            data=data, 
            headers={"Content-Type": "application/json"}
        )
        
        # 4. Open connection and send data
        with urllib.request.urlopen(req, timeout=30) as response:
            # 5. Read and parse the server response
            res_json = json.loads(response.read().decode("utf-8"))
            return res_json.get("response", "").strip()
            
    except Exception as e:
        # 6. Graceful error handling fallback
        return "The information is not in the inbox."

