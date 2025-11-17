## ReAct + Plan-and-Execute — Minimal AI Agent Demo

This project is a minimal demonstration of how an AI agent can reason and interact with external tools.
It implements the **ReAct (Reasoning + Acting)** pattern and integrates a **Plan-and-Execute** workflow to build a clear, extensible agent framework.

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)]()
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)]()
[![ReAct Workflow](https://img.shields.io/badge/Agent-ReAct-orange.svg)]()
[![Plan & Execute](https://img.shields.io/badge/Pattern-Plan--and--Execute-yellow.svg)]()
[![LLM Powered](https://img.shields.io/badge/LLM-OpenRouter-purple)]()
[![uv Package Manager](https://img.shields.io/badge/Powered%20by-uv-black)]()
[![OpenAI Compatible](https://img.shields.io/badge/LLM_Adapter-OpenAI%20API-blueviolet)]()

## Quick Start
### 1. Create a .env file in the same folder as README.md and add your API key:
```
OPENROUTER_API_KEY=
LLM_MODEL=
```
You can also modify `react_agent/core/llm_client.py` if you want to use a different LLM provider.
### 2. Install uv (Python package manager):
```
pip install uv
```
### 3. Install dependencies:
```
uv sync
```
### 4. Run the agent 
In the project root (top-level directory), passing the folder you want the agent to work inside:
```
uv run react-agent ./tests 
```
You can replace `./tests` with any directory you want the agent to operate in.

## What is ReAct
Paper: https://arxiv.org/abs/2210.03629
<br>
ReAct is a framework that lets LLMs operate in a loop of:

- Thought — the model reasons about the next step
- Action — the model calls a tool or performs an operation
- Observation — the agent receives the tool result
- Final Answer — the agent concludes the task

This loop enables the model to interact with the outside world instead of only generating text.

<br>

<p align="center">
  <img src="./assets/svg/react_workflow.svg" width="650">
</p>

## What is Plan-And-Execute
Reference: https://langchain-ai.github.io/langgraph/tutorials/plan-and-execute/plan-and-execute/



## 

keeps ReActAgent focused on:
- rendering the system prompt
- orchestrating messages
- parsing tool calls
- running tools



## Parser

Traditional way:
regex and state machine
```
run("hello, world", (1, 2, 3), "line1\nline2", [1, (2, 3)])
```

we only want to parse like
```
"hello, world"
(1, 2, 3)
"line1\nline2"
[1, (2, 3)]
```

### 🚀 How a finite state machine solve?
1 Tracks whether we are in a quoted string. <br>
2 Tracks whether we are in nested parenthesis. <br>
3 Only treats a `,` a real argument seperator if:

  - not inside quoted string, **and**
  - `paren_depth = 0`

| Variable      | Purpose                                         |
| ------------- | ----------------------------------------------- |
| `args`        | Final parsed argument list                      |
| `current_arg` | The argument being built as characters are read |
| `in_string`   | True if inside `"..."` or `'...'`               |
| `string_char` | Which quote started the string (`"` or `'`)     |
| `i`           | Character index                                 |
| `paren_depth` | Count of nested parentheses                     |


### Analsis of parsing rules
```python
if char == string_char and (i == 0 or args_str[i-1] != '\\'):
```

#### 🧪 Case 1: A normal string
```
"hello world"
            ^
```

#### 🧪 Case 2: Contain escaped char
```
"hello \"world\""
        ^
```
This `"` is escaped by `\` before it, so it should NOT end the string.

#### 🧩 Python would access [-1]
```
if i == 0:
    treat quote normally (not escaped)
```

`i == 0` is just for safty because we must make the flag `in_String = True` first, which requires at lease one char and `i` would then goes to 1. After finding another end, we just check which type `'` or `"` and is not escaped. But at then, `i` would always greater than 1.

#### 🧩 Parsing insight
A DFA cannot recognize languages like

$\{a^nb^n \ |\  n ≥ 0\}$

because it has no memory
but our parser
```py
paren_depth = 0

if char == '(':
    paren_depth += 1
elif char == ')':
    paren_depth -= 1
```

This is like `Pushdown automaton (PDA)` with a simplified “stack”
(even though we only store an integer depth, not the full stack of symbols)

### Common bug

#### Parse error
```
TypeError: write_to_file() takes 2 positional arguments but 97 were given
```

Because we encounter edge cases like:

```
write_to_file("tests/snake.html", <html><head><title>Snake Game</title>...</html>)
```
or
```
write_to_file("tests/snake.html",
"<html><head>...</head>",
"<body>...</body>",
"..."
)
```

However, the parser is for: \(It is important to know how you analyze LLM output\)

```
write_to_file("tests/snake.html", "<html><head>...</head><body>...</body></html>")
```
We can resort to other approaches, but in this parser case we can have two system design: <br>

**Should we revise system prompt or parser code?**

We should do both <br>
- System prompt = contract for the model. 
- Code = firewall: validate, repair, or reject bad actions.

We tell the model the rules in the system prompt also assume it will sometimes break them anyway, and add checks / fixes in code.

#### use echo and the string cannot be parsed
```
[22:48:48] Raw Model Reply: <thought>The CSS file has been successfully created in the `/tmp/snake_game` directory. Now, I need to create the JavaScript file to implement the functionality of the Snake game.</thought><action>run_terminal_command("echo 'const canvas = document.getElementById(\"gameCanvas\");\\nconst ctx = canvas.getContext(\"2d\");\\n\\nlet snake = [\\n    { x: 10, y: 10 }\\n];\\nlet direction = { x: 0, y: 0 };\\n\\nfunction gameLoop() {\\n    ctx.clearRect(0, 0, canvas.width, canvas.height);\\n    ctx.fillStyle = \"lime\";\\n    snake.forEach(part => {\\n        ctx.fillRect(part.x, part.y, 10, 10);\\n    });\\n    // Move Snake Logic Here\\n    requestAnimationFrame(gameLoop);\\n}\\n\\ndocument.addEventListener(\"keydown\", event => {\\n    if (event.key === \"ArrowUp\") direction = { x: 0, y: -10 };\\n    if (event.key === \"ArrowDown\") direction = { x: 0, y: 10 };\\n    if (event.key === \"ArrowLeft\") direction = { x: -10, y: 0 };\\n    if (event.key === \"ArrowRight\") direction = { x: 10, y: 0 };\\n});\\n\\ngameLoop();' > /tmp/snake_game/snake.js")</action>
```
after parsed:
```
body {\
    display: flex;\
    justify-content: center;\
    align-items: center;\
    height: 100vh;\
    background-color: #000;\
}\
\
canvas {\
    border: 1px solid #fff;\
}
```

#### Tool design
```
with open(file_path, "r", encoding="utf-8") as f:
    f.write(content)
```
Make sure grant the tool/ file used with correct mode/ permission
```
[Errno 2] No such file or directory
```
The agent to believe the directory didn't exist,

#### Observation design
Key rules:
- Generated by our system, never by the model. 
- Provided after an <action> executes.

We should make sure to send back observation, containing tool output, error messages, or command results. Otherwise the model cannot make furthur adjustment. <br>

