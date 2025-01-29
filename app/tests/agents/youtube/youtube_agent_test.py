import os
from dotenv import load_dotenv
import sys
from app.common.youtube.youtube_search import YouTubeSearcher, VideoStats
from app.configs.settings import Settings
from app.configs.logging_config import get_logger
from app.common.storage.file_storage import FileStorage
from app.common.storage.storage_interface import Storage
from app.common.storage.storage_factory import StorageFactory
from app.common.data_converters.json_helper import JsonHelper

# Create a logger
logger = get_logger(__name__)


def test_download_youtube_videos():
    """
    A functional test that makes actual API call or process a saved JSON file based on the value of 'use_test_data' field. 
    The function should validate content of returned object that is a list of dictionaries with video details.
    """
    use_test_data = Settings.use_test_data
    logger.info("Running test_get_youtube_videos. Using test data? " + str(use_test_data))

    logger.info("Use TEST DATA in OS: " + str(os.environ.get("USE_TEST_DATA")))
    logger.info("Use TEST DATA in Settings: " + str(Settings.use_test_data))
    # Initialize storage and searcher
    storage = StorageFactory.get_storage(Settings.storage_type, Settings.test_files_dir)
    searcher = YouTubeSearcher(Settings.youtube_api_key, storage)
    search_term = "asthma treatments"
    results = []
    
    if use_test_data:        
        logger.info("Getting youtube videos from local file")
        test_files_dir = os.path.join(Settings.project_root, Settings.test_files_dir)
        storage = StorageFactory.get_storage("local", test_files_dir)
        file_content = storage.get("youtube_result_single.json")
        if file_content is None:
            raise ValueError("Could not read youtube-result-single.json")
        results = JsonHelper.json_to_list(file_content, VideoStats)
    else:
        logger.info("Getting youtube videos for search term from Youtube: " + search_term)
        results = searcher.search_videos(search_term)
    
    # logger.debug("Fetched result: " + str(results))

    assert isinstance(results, list), "Expected a list of results"
    assert len(results) > 0, "Expected at least one result"

    video_data = results[0]
    logger.debug("Fetched Video: " + str(video_data))

    assert hasattr(video_data, "video_id"), "Expected result to have video_id"
    assert hasattr(video_data, "title"), "Expected result to have a title"
    assert hasattr(video_data, "description"), "Expected result to have a description"
    assert hasattr(video_data, "view_count"), "Expected result to have a view count"
    assert hasattr(video_data, "like_count"), "Expected result to have a like count"
    assert hasattr(video_data, "favorite_count"), "Expected result to have a favorite count"
    assert hasattr(video_data, "comment_count"), "Expected result to have a comment count"
    assert hasattr(video_data, "thumbnails"), "Expected result to have thumbnails list"
    assert hasattr(video_data, "transcript"), "Expected result to have a transcript"


def test_load_youtube_videos_from_files():
    """
    A functional test that loads youtube videos from a file
    """
    input = "Health"
    storage = StorageFactory.get_storage(Settings.storage_type, Settings.test_files_dir)
    searcher = YouTubeSearcher(Settings.youtube_api_key, storage)
    keywords = {"health-physical health-strength training": "physical health"}
    if keywords is None:
        raise ValueError("Keywords are None")
    
    videos = searcher.load_youtube_videos_from_files(keywords)

    assert isinstance(videos, list), "Expected a list of results"
    assert len(videos) > 0, "Expected at least one result"


# Run the test
# if modules are not found, add the path to the modules to the PYTHONPATH
# export PYTHONPATH=$(pwd)
if __name__ == "__main__":
    key = Settings.youtube_api_key
    print("KEY " + key)
    test_download_youtube_videos()
