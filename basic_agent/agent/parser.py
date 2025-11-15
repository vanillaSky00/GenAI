from dataclasses import dataclass
import re
from typing import Optional, List, Tuple

@dataclass
class MatchedStep:
    thought: Optional[str]
    action: Optional[str]
    final_answer: Optional[str]

def match_react_output(content: str) -> MatchedStep:
    thought = None
    action = None
    final_answer = None
    
    thought_match = re.search("", content, re.DOTALL)
    if thought_match:
        thought = thought_match.group(1).strip()
        
    final_match = re.search("", content, re.DOTALL)
    if final_match:
        final_answer = final_match.group(1).strip()
    
    action_match = re.search("", content, re.DOTALL)
    if action_match:
        action = action_match.group(1).strip()
    
    return MatchedStep(thought=thought, action=action, final_answer=final_answer)


def parse_action(code_str: str) -> Tuple[str, List[str]]:
    
    pass


def _parse_single_arg(arg_str: str):
    pass