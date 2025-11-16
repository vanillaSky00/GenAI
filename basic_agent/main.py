import os

import click

from agent.tools import get_default_tools
from agent.agent import ReActAgent
from agent.llm_client import LLMClient
from global_utils import get_llm_model_name

@click.command()
@click.argument('project_directory',
               type=click.Path(exists=True, file_okay=True, dir_okay=True))
def main(project_directory):
    
    project_dir = os.path.abspath(project_directory)
    model_name = get_llm_model_name()
    
    tools = get_default_tools()
    agent = ReActAgent(
        tools=tools,
        model=model_name,
        client=LLMClient(model=model_name),
        project_directory=project_dir,
    )
    
    task = input("Input the task: ")
    
    final_answer = agent.run(task)
    
    print(f"\n\n✅ Final Answer：{final_answer}")

if __name__ == "__main__":
    main()