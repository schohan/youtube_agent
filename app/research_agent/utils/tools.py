from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

from app.tools.content.youtube import Youtube

def search_youtube_videos(search_term, api_key, max_results=10):
    return Youtube.search_youtube_videos(search_term, api_key, max_results)

 