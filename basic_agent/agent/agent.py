# basic_agent/agent/agent.py
import inspect
import os
from string import Template
from typing import Dict, Any, List

from .tools import Tool
from .llm_client import LLMClient
from basic_agent.prompt_template import react_system_prompt_template
import basic_agent.utils as utils  


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
            
            thought = self._check_thought(content)
            final = self._check_final(content)
            
            if final is not None:
                return final
            
            action_str = self._check_action(content)
            tool_name, args = self.parse_action(action_str)
            
            observation = self._run_tool(tool_name, args)
            obs_msg = f"<observation>{observation}</observation>"
            messages.append({"role": "user", "content": obs_msg})
            
            
    def get_tool_list(self):
        """Show the defined tools to the agent, with function signatures and docs."""
        tool_descriptions = []
        tool_descriptions = []
        for func in self.tools.values():
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
    
    
    def parse_action(self):
        pass
    
    def _parse_single_arg(self):
        pass
    
    def _check_thought(self):
        pass
    
    def _check_final(self):
        pass
    
    def _check_action(self):
        pass
    
    def _run_tool(self):
        pass
    
