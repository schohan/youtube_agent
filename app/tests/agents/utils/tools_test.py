import os
from dotenv import load_dotenv
import sys
from app.configs.logging_config import get_logger
from app.configs.settings import Settings

# Ensure the PYTHONPATH environment variable is set to the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

# Create a logger
logger = get_logger(__name__)

# Load environment variables from .env file
load_dotenv()

from app.agents.utils.tools import search_youtube_videos 
from app.toolhelpers.storage.file_storage import FileStorage
from app.toolhelpers.storage.storage_interface import Storage
from app.toolhelpers.storage.storage_factory import StorageFactory

use_test_data = Config.use_test_data

def test_download_youtube_videos():
    """
    A functional test that makes actual API call or process a saved JSON file based on the value of 'use_test_data' field. 
    The function should validate content of returned object that is a list of dictionaries with video details.
    """
    logger.info("Running test_get_youtube_videos. Using test data? " + str(use_test_data))
    
    search_term = "asthma treatments"
    results = []
    
    if use_test_data:        
        logger.info("Getting youtube videos from local file")
        test_files_dir = test_files_dir = os.path.join(Config.project_root, Config.test_files_dir)
        storage = StorageFactory.get_storage("local", test_files_dir)
        results.append (storage.get("youtube-result-single.json"))
    else:
        logger.info("Getting youtube videos for search term from Youtube: " + search_term)
        results = search_youtube_videos(search_term)
    
    logger.debug("Fetched result: " + str(results))

    assert isinstance(results, list), "Expected a list of results"
    assert len(results) > 0, "Expected at least one result"
    
    assert "videoId" in results[0], "Expected result to have videoid"
    assert "title" in results[0], "Expected result to have a title"
    assert "description" in results[0], "Expected data to have a description"
    assert "viewCount" in results[0], "Expected result to have a view count"
    assert "likeCount" in results[0], "Expected result to have a like count"
    assert "favoriteCount" in results[0], "Expected result to have a favorite count"
    assert "commentCount" in results[0], "Expected result to have a comment count"
    assert "thumbnails" in results[0], "Expected result to have thumbnails list"
    assert "captions" in results[0], "Expected result to have a captions list"
    assert "transcript" in results[0], "Expected result to have a transcript"


# Run the test
# if modules are not found, add the path to the modules to the PYTHONPATH
# export PYTHONPATH=$(pwd)
if __name__ == "__main__":
    # use_test_data = False
    key = Settings.youtube_api_key
    print("KEY " + key)
    test_download_youtube_videos()