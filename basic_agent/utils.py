from dotenv import load_dotenv
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
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("Cannot find OPENAI_API_KEY, please make sure .env is correctly configured")
    
    return api_key