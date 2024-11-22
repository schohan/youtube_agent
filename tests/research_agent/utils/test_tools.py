import os
import pytest
from dotenv import load_dotenv
import sys
from app.configs.logging_config import get_logger
from app.configs.app_config import Config

# Ensure the PYTHONPATH environment variable is set to the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

# Create a logger
logger = get_logger(__name__)

# Load environment variables from .env file
load_dotenv()

from app.research_agent.agent import get_youtube_videos
from app.tools.storage.file_storage import FileStorage
from app.tools.storage.storage_interface import Storage
from app.tools.storage.storage_factory import StorageFactory


def test_get_youtube_videos(use_test_data = True):
    """
    A functional test for get_youtube_videos function that makes actual API call. 
    The function should validate content of returned object that is a list of dictionaries with video details.
    """
    logger.info("Running test_get_youtube_videos")
    
    search_term = "asthma treatments"
    results = []
    
    if use_test_data:        
        test_files_dir = test_files_dir = os.path.join(Config.project_root, Config.test_files_dir)
        logger.info("File path " + test_files_dir)
        storage = StorageFactory.get_storage("local", test_files_dir)
        logger.info("*** File path 2 " + str(storage.has_item("youtube-result-single.json")))
        results.append (storage.get("youtube-result-single.json"))
    else:
        results = get_youtube_videos(search_term)
    
    print(results)

    assert isinstance(results, list), "Expected a list of results"
    assert len(results) > 0, "Expected at least one result"
    
    assert "id" in results[0], "Expected result to have video id"
    assert "title" in results[0], "Expected result to have a title"
    assert "views" in results[0], "Expected result to have a view count"
    assert "thumbnail" in results[0], "Expected result to have a thumbnail"
    assert "captions" in results[0], "Expected result to have a captions list"
    assert "transcript" in results[0], "Expected result to have a transcript"


# Run the test
# if modules are not found, add the path to the modules to the PYTHONPATH
# export PYTHONPATH=$(pwd)
if __name__ == "__main__":
    key = os.environ.get("YOUTUBE_API_KEY", "")
    print("KEY " + key)
    pytest.main()