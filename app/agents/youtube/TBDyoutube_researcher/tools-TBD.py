from googleapiclient.discovery import build
from openai import api_key
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.tools import tool
from app.research_agent.utils.state import VideoList
from app.toolhelpers.content.youtube import Youtube, YoutubeSnippet
from app.configs.settings import Config

@tool
def search_youtube_videos(search_term):
    """
    Search youtube videos based on a search term

    Args:
        search_term (str): The query to search for
        api_key (str): The youtube api key
        max_results (int): The maximum number of results to return

    Returns:
        results (list): A list of dictionaries with video details
    """
    # TODO - get the api key from the config based on current llm
    api_key = Config.openai_api_key

    return Youtube.search_youtube_videos(search_term, api_key, Config.max_youtube_results)

 
@tool
def video_summarizer(videos: VideoList):
    """
    Summarize a youtube video

    Args:
        video_id (str): The youtube video id

    Returns:
        summary (str): The summary of the video
    """
    summaries = []
    return summaries




tools = [search_youtube_videos, video_summarizer]
