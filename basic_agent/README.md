## ReAct + Plan-and-Execute — Minimal AI Agent Demo

This project is a simple demo showing how an AI agent can reason and interact with external tools.
It follows the ReAct (Reasoning + Acting) workflow and combines it with the Plan-and-Execute pattern to build an extendable agent framework.


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
  <img src="./assets/ReAct_workflow.svg" width="650">
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

We are more likely use `Pushdown automaton (PDA)` with a simplified “stack”
(even though we only store an integer depth, not the full stack of symbols)