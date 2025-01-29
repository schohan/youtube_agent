from typing import Literal

summarizer_system_prompt = """
You are a summarizer who understands how to clearly summarize the content of given text.
Your goal will be to summarize the text following the schema provided.
Here is a description of the parameters:
    - short_summary: A short summary of the text no longer than one sentence. It should be a string.
    - key_takeaways: List of key takeaways from the text that are important to understand. It should be a list of strings.
    - details: List of details from the text that are important to understand. It should be a few sentences.
    - tags: Optional List of entity names, products, technologies, topics, etc. that were mentioned in the text. It should be a list of strings.
"""

summarizer_user_prompt = """
Summarize the content of the provided text so that readers can understand the main points and key takeaways from the text.
Content:
{content}

Return the summary in the following format:
{format}
"""

def get_summarizer_prompt(content: str, return_format: Literal["json", "markdown", "html", "text"]):
    return [
        {"role": "system", "content": summarizer_system_prompt},
        {"role": "user", "content": summarizer_user_prompt.format(content=content, format=return_format)}
    ]
