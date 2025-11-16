from dataclasses import dataclass
import re
import ast
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
    
    thought_match = re.search(r"<thought>(.*?)</thought>", content, re.DOTALL)
    if thought_match:
        thought = thought_match.group(1).strip()
        
    final_match = re.search(r"<final_answer>(.*?)</final_answer>", content, re.DOTALL)
    if final_match:
        final_answer = final_match.group(1).strip()
    
    action_match = re.search(r"<action>(.*?)</action>", content, re.DOTALL)
    if action_match:
        action = action_match.group(1).strip()
    
    return MatchedStep(thought=thought, action=action, final_answer=final_answer)



"""
    Parse usage:
    
    func_name, args = parse_action('write_to_file("foo,bar.txt", 123, [1, 2])')
    # func_name = "write_to_file"
    # args      = ["foo,bar.txt", 123, [1, 2]]
    self.tools[func_name].handler(*args)
"""

def parse_action(code_str: str) -> Tuple[str, List[str]]:
    match = re.match(r'(\w+)\((.*)\)', code_str, re.DOTALL)
    if not match:
        raise ValueError("Invalid function call syntax")
    
    func_name = match.group(1)
    args_str = match.group(2).strip()
    
    args = []
    current_arg = ""
    in_string = False
    string_char = None
    i = 0
    paren_depth = 0
    
    # TODO: Customized state machine
    while i < len(args_str):
        char = args_str[i]
        
        if not in_string:  
            if char in ["'",'"']:
                in_string = True
                string_char = char
                current_arg += char
            elif char == '(':
                paren_depth += 1
                current_arg += char
            elif char == ')':
                paren_depth -= 1
                current_arg += char
            elif char == ',' and paren_depth == 0:
                args.append(_parse_single_arg(current_arg.strip()))
                current_arg = ""
            else:
                current_arg += char
        else:
            current_arg += char
            if char == string_char and (i == 0 or args_str[i-1] != '\\'):
                in_string = False
                string_char = None
        
        i+=1

        # Add last arg
        if current_arg.strip(): # prevent trailing space
            args.append(_parse_single_arg(current_arg.strip()))
            
    return func_name, args      

def _parse_single_arg(arg_str: str):
    arg_str = arg_str.strip()
    
    # If arg is str symbol
    if (arg_str.startswith('"') and arg_str.endswith('"')) or \
       (arg_str.startswith("'") and arg_str.endswith("'")):
           inner_str = arg_str[1:-1]
           
           inner_str = inner_str.replace('\\"', '"').replace("\\'", "'")
           inner_str = inner_str.replace('\\n', '\n').replace('\\t', '\t')
           inner_str = inner_str.replace('\\r', '\r').replace('\\\\', '\\')
           return inner_str
       
    # Other type
    try:
        return ast.literal_eval(arg_str)
    except (SyntaxError, ValueError):
        return arg_str