from dotenv import load_dotenv
from datetime import datetime
import os, platform

def get_operating_system_name() -> str:
    os_map = {
        "Darwin": "macOS",
        "Windows": "Windows",
        "Linus": "Linux",
    }
    
    return os_map.get(platform.system(), "Unknown")

def get_api_key() -> str:
    load_dotenv()    
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        raise ValueError("Cannot find OPENROUTER_API_KEY, please make sure .env is correctly configured")
    
    return api_key

def get_llm_model_name() -> str:
    load_dotenv()    
    llm_model_name = os.getenv("LLM_MODEL")
    
    if not llm_model_name:
        raise ValueError("Cannot find LLM_MODEL, please make sure .env is correctly configured")
    
    return llm_model_name

def write_log(message: str, log_dir="log"):
    os.makedirs(log_dir, exist_ok=True)
    
    filename = datetime.now().strftime("%Y-%m-%d") + ".txt"
    log_path = os.path.join(log_dir, filename)
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)
        
    return log_path
        