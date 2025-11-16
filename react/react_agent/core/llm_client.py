from openai import OpenAI
from react_agent import global_utils as utils

class LLMClient:
    def __init__(self, model):
        self.model = model
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=utils.get_api_key(),
        )
        
    def chat(self, messages):
        print("\n\nWaiting for model")
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        
        content = response.choices[0].message.content
        return content
    