from typing import Literal

summarizer_system_prompt = """
You are a summarizer who understands how to clearly summarize the content of a video given to you as transcript.
"""

summarizer_user_prompt = """
Summarize the content of a video so that readers can understand the main points and key takeaways from the video.
content:
{content}

Return the summary in the following format:
{format}
"""

def get_summarizer_prompt(content: str, return_format: Literal["markdown", "html", "text"]):
    return [
        {"role": "system", "content": summarizer_system_prompt},
        {"role": "user", "content": summarizer_user_prompt.format(content=content, format=return_format)}
    ]
