
from click import prompt
from app.common.llm.llm_factory import LLMFactory
from app.common.llm.llm_interface import LLM
from app.configs.settings import Settings
from langchain_openai import ChatOpenAI
from app.prompts.summarizer_prompts import get_summarizer_prompt

class ContentSummarizer:

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm



    def summarize_content(self, content: str):
        prompt = get_summarizer_prompt(content, "markdown")
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
   
  
    summary = content_summarizer.summarize_content(content=content)
    print(summary)