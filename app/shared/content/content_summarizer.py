
from app.shared.llm.llm_factory import LLMFactory

class ContentSummarizer:

    def __init__(self, prompt: str, llm: str):
        self.prompt = prompt
        self.llm = llm

    def summarize_content(self, content: str):
        pass