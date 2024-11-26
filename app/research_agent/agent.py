from curses import raw
from app.research_agent.utils.nodes import graph
from app.research_agent.utils.tools import search_youtube_videos
from app.configs.app_config import Config
from pathlib import Path

# import os

def download_youtube_videos(query: str):
    """
    Get youtube videos based on a query

    Args:
        query (str): The query to search for

    Returns:
        results (list): A list of dictionaries with video details
    """

    api_key = Config.youtube_api_key # os.environ.get("YOUTUBE_API_KEY")
    max_results = Config.max_youtube_results # int(os.environ.get("MAX_YOUTUBE_RESULTS", 10))

    print("Config.youtube_api_key " + api_key)

    results = search_youtube_videos(query, api_key, max_results=max_results)
    return results


def process_raw_videos():
    """
    Process raw downloaded youtube videos from configured raw video location. Processing involves:
     a. Summarizing videos using transcript
     b. Save processed objects along with metadata to storage for use by application

    Args:
        None

    Returns:
        None
    """
    # 
    # process all files in the given directory. Use supplied functions to process the files
    # TODO: Implement this function  
    




# def stream_graph_updates(user_input: str):
#     for event in graph.stream({"messages": [("user", user_input)]}):
#         for value in event.values():
#             print("Assistant:", value["messages"][-1].content)
#             return value["messages"][-1].content


#download_youtube_videos("asthma treatments")