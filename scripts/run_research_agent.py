# Test driver for the app. Use this to run the app modules locally without running the server
# from dotenv import load_dotenv
# import os
# #load env variables from .evn file
# load_dotenv()
import os

from numpy import add
from app.research_agent.agent import start_agent
from app.configs.settings import Config
from app.toolhelpers.storage.file_storage import FileStorage
from app.toolhelpers.data_converters.json_helper import JsonHelper
from scripts.add_root import add_project_root_to_sys_path

add_project_root_to_sys_path()

# def search_youtube_videos_direct(search_term):
#     """ 
#         Search youtube videos based on a search term directly using the Youtube class
#         Args:
#             search_term (str): The query to search for
#             api_key (str): The youtube api key
#             max_results (int): The maximum number of results to return
#         Returns:
#             results (list): A list of dictionaries with video details
#     """
#     return get_and_process_youtube_videos(search_term)

def main():
    """
    Main function to run the agent
    """
    keywords = ['how to start a startup', 'startup funding', 'startup business plan', 'entrepreneurship tips', 'startup success stories', 'startup challenges', 'startup marketing strategies', 'startup legal requirements', 'startup team building', 'startup growth strategies']
    results = start_agent(keywords, 1)
    
    print(f"Final Topics  {results['topics']}")
    
    storage = FileStorage(os.path.join(Config.project_root, Config.test_files_dir))
    
    storage.set("youtube_results-temp.json", JsonHelper.list_to_str([results]))



if __name__ == "__main__":
    """
    Test driver for the app. Use this to run the agent without the API server.    
    """
    main()
    # #results = search_youtube_videos_direct("asthma treatments")
    # keywords = ['how to start a startup', 'startup funding', 'startup business plan', 'entrepreneurship tips', 'startup success stories', 'startup challenges', 'startup marketing strategies', 'startup legal requirements', 'startup team building', 'startup growth strategies']
    # results = start_agent(keywords, 1)
    # print(f"Final Topics  {results['topics']}")
    # # storage = FileStorage(os.path.join(Config.project_root, Config.test_files_dir))
    # storage.set("youtube_results-temp.json", JsonHelper.list_to_str(results))

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