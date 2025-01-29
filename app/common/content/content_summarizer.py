
from click import prompt
from app.common.llm.llm_factory import LLMFactory
from app.common.llm.llm_interface import LLM
from app.configs.settings import Settings
from langchain_openai import ChatOpenAI
from app.prompts.summarizer_prompts import get_summarizer_prompt
from typing import Literal
class ContentSummarizer:

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm



    def summarize_content(self, content: str, return_format: Literal["json", "markdown", "html", "text"] = "json"):
        if content is None or content == "":
            raise ValueError("Content is required")
        
        prompt = get_summarizer_prompt(content, return_format)
        summary = self.llm.invoke(prompt)
        return summary




# ==============================
if __name__ == "__main__":
    llm = LLMFactory.get_llm(Settings.summarizer_llm)
    if llm is None:
        raise ValueError("LLM is not initialized")
    
    content_summarizer = ContentSummarizer(llm)
    with open("data/test/transcript.txt", "r") as file:
        content = file.read()
   
    
    summary = content_summarizer.summarize_content(content, "json")
    print(summary)