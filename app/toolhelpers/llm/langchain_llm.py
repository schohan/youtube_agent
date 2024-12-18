from app.toolhelpers.llm.llm_interface import LLM
from typing import Any

from langchain_openai import ChatOpenAI
from app.configs.app_config import Config


class OpenAILLM(LLM):
    """
    Langchain LLM class that provides access to multiple LLMs via single interface.
    """

    def __init__(self, **kwargs):
        self.llm = ChatOpenAI(model=Config.model_name, temperature=Config.model_temperature) 

    def invoke(self, input) -> Any:
        return self.llm.invoke(input)

    def stream(self, input) -> str:
        return "OpenAI LLM stream"

    def chat(self, input) -> str:
        return "OpenAI LLM chat"
    
