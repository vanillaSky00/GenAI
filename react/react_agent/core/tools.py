from dataclasses import dataclass
from typing import Callable, Dict

@dataclass
class Tool:
    name: str
    description: str
    handler: Callable[..., str]

def read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def write_to_file(file_path: str, content: str) -> str:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.replace("\\n", "\n"))
    return "Successfully written"

def run_terminal_command(command):
    import subprocess
    run_result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return f"Successfully executed + {run_result}" if run_result.returncode == 0 else run_result.stderr

def get_default_tools() -> Dict[str, Tool]:
    return {
        "read_file": Tool(
            name="read_file",
            description="Read a text file from disk. Args: path: str.",
            handler=read_file,
        ),
        "write_to_file": Tool(
            name="write_to_file",
            description="Write text to a file. Args: path: str, content: str.",
            handler=write_to_file,
        ),
        "run_terminal_command": Tool(
            name="run_terminal_command",
            description="Run a shell command and return its output. Args: cmd: str.",
            handler=run_terminal_command,
        ),
    }
    
    
# TODO: memory_search(), memory_write(), db schema