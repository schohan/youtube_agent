from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.tools import tool
from app.tools.content.youtube import Youtube


def search_youtube_videos(search_term, api_key, max_results=10):
    return Youtube.search_youtube_videos(search_term, api_key, max_results)



def find_search_terms_for_topic(topic):
    return ["asthma-term1", "asthma-term2"] if topic == "asthma" else ["generic-term3", "generic-term4"]



def summarizer(video_id):
    return "summary of video"





 

