# basic_agent/agent/agent.py
import inspect
import os
from string import Template
from typing import Dict, List

from .tools import Tool
from .llm_client import LLMClient
from .policy import required_permissions
from .parser import match_react_output, parse_action
from react_agent import global_utils as utils
from react_agent.prompt_template import react_system_prompt_template  


class ReActAgent:
    def __init__(self, tools: Dict[str, Tool], model: str, client: LLMClient, project_directory: str):
        self.tools = tools
        self.model = model
        self.client = client
        self.project_directory = project_directory
    
    def run(self, user_input: str):
        messages = [
            {"role": "system", "content": self.render_system_prompt(react_system_prompt_template)},
            {"role": "user", "content": f"<question>{user_input}</question>"},
        ]
        
        while True:
            content = self.call_model(messages)
            
            matched = match_react_output(content)
            
            if matched.thought:
                print(f"\n\n💭 Thought: {matched.thought}")
                
            if matched.final_answer:
                return matched.final_answer
            
            if not matched.action:
                raise RuntimeError("Model not output <action>")
            
            tool_name, args = parse_action(matched.action)
            print(f"\n\n Action: {tool_name}({', '.join(args)})")
            
            args = self._sanitize_action(tool_name, args)
            
            # Only terminal-related tool need explicily request
            should_continue = input(f"\n\nStill continue? (Y/N) ") if tool_name in required_permissions else "y"
            if should_continue.lower() != 'y':
                print("\n\n Operation cancelled")
                return "Operation terminated"
            
            try:
                observation = self._run_tool(tool_name, args)
            except Exception as e:
                observation = f"Tool errors: {str(e)}"
            
            print(f"\n\n🔍 Observation：{observation}")        
            obs_msg = f"<observation>{observation}</observation>"
            messages.append({"role": "user", "content": obs_msg})
            
            
    def get_tool_list(self):
        """Show the defined tools to the agent, with function signatures and docs."""
        tool_descriptions = []
        for tool in self.tools.values():
            func = tool.handler
            name = func.__name__
            signature = str(inspect.signature(func))
            doc = inspect.getdoc(func)
            tool_descriptions.append(f"- {name}{signature}: {doc}")
        return "\n".join(tool_descriptions)
    
    
    def render_system_prompt(self, system_prompt_template: str) -> str:
        """Generate the final system prompt with dynamic info (tools, OS, files)."""
        tool_list = self.get_tool_list()
        file_list = ", ".join(
            os.path.abspath(os.path.join(self.project_directory, f))
            for f in os.listdir(self.project_directory)
        )
        
        return Template(system_prompt_template).substitute(
            operating_system=utils.get_operating_system_name(),
            tool_list=tool_list,
            file_list=file_list,
        )
    
    
    def call_model(self, messages):
        content = self.client.chat(messages)
        messages.append({"role": "assistant", "content": content})
        return content
    
    
    def _run_tool(self, tool_name: str, args: List[str]):
        return self.tools[tool_name].handler(*args)
    
    
    def _sanitize_action(self, tool_name: str, args: List[str]):
        if tool_name == "write_to_file":
            if len(args) >= 2:
                file_path = args[0]
                content = "".join(args[1:])
                return [file_path, content]
    
        return args