# Test driver for the app. Use this to run the app modules locally without running the server
# from dotenv import load_dotenv
# import os
# #load env variables from .evn file
# load_dotenv()
import os
from app.research_agent.agent import get_youtube_videos
from app.tools.content.youtube import Youtube
from app.configs.app_config import Config
from app.tools.storage.file_storage import FileStorage
from app.tools.data_converters.json_helper import JsonHelper

def search_youtube_videos_direct(search_term, api_key, max_results=10):
    """ 
        Search youtube videos based on a search term directly using the Youtube class
        Args:
            search_term (str): The query to search for
            api_key (str): The youtube api key
            max_results (int): The maximum number of results to return
        Returns:
            results (list): A list of dictionaries with video details
    """
    return Youtube.search_youtube_videos(search_term, api_key, max_results)



if __name__ == "__main__":
    """
    Test driver for the app. Use this to run the app modules locally without running the server.    
    """
    key = Config.youtube_api_key 
    if key:
        print("KEY " + key)
    else:
        print("YOUTUBE_API_KEY not found in environment variables")
    results = search_youtube_videos_direct("asthma treatments", key, 1)
    print(results)
    storage = FileStorage(os.path.join(Config.project_root, Config.test_files_dir))
    storage.set("youtube_results-temp.json", JsonHelper.list_to_str(results))

# Expected output:




# # Example usage:
# import os
# from dotenv import load_dotenv
# #load env variables from .evn file
# load_dotenv()

# api_key = os.environ.get("YOUTUBE_API_KEY", "No API KEY found")
# print("API key "+ api_key)
# search_term = "Python basics"
# print(search_youtube_videos(search_term, api_key, 1))