##
This is a demo for basic ai agent framwork, based on ReeAct and Plan And Execute


## What is ReAct
Paper: https://arxiv.org/abs/2210.03629
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
https://langchain-ai.github.io/langgraph/tutorials/plan-and-execute/plan-and-execute/

