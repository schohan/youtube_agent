from app.common.storage.file_storage import FileStorage
from app.configs.settings import Settings
from app.configs.logging_config import get_logger
from app.common.storage.storage_factory import StorageFactory
import os
import json


# Create a logger
logger = get_logger(__name__)

def test_set():
    to_save = """
    [
        {
            "title": "Learn Python in Less than 10 Minutes for Beginners (Fast &amp; Easy)", 
            "views": "343776", 
            "thumbnail": "https: //i.ytimg.com/vi/fWjsdhR3z3c/default.jpg", 
            "captions": [{
                "id": "AUieDaZak5T6m2XnS5ioWt3GXE5QOsSrIMEhwiO3DYWlB2ZwFIY", "language": "en", "name": ""
            }], 
            "transcript": "what is up guys in this video i'm going to be showing you how you can get started with python in less than 10 minutes and i'm going to be using python 3.8 for this along with pycharm as my code editor you can just" 
        }
    ]
    """
    test_files_dir = test_files_dir = os.path.join(Settings.project_root, Settings.test_files_dir)      
    storage = StorageFactory.get_storage("local", test_files_dir)
    storage.set("youtube-test-file-temp.json", to_save)   
    logger.info("Saved test data to file")


def test_has_item():
    test_files_dir = test_files_dir = os.path.join(Settings.project_root, Settings.test_files_dir)      
    storage = StorageFactory.get_storage("local", test_files_dir)
    assert storage.has_item("youtube_result_single.json"), "Expected file to exist in storage"
    logger.info("File exists in storage")

    assert not storage.has_item("nonexistent_file.json"), "Expected file to not exist in storage"
    logger.info("File does not exist in storage")



def test_get():
    test_files_dir = test_files_dir = os.path.join(Settings.project_root, Settings.test_files_dir)      
    storage = StorageFactory.get_storage("local", test_files_dir)
    data_str = storage.get("youtube_result_single.json")
    print(data_str)
    
    try:
        if data_str is None:
            raise ValueError("No data returned from storage")
        data = json.loads(data_str)
        logger.info("Retrieved test data from file")
        print(data)
        assert data is not None, "Expected data to be returned"
        assert len(data) > 0, "Expected data to have at least one item"
        assert "title" in data[0], "Expected data to have a title"
        assert "description" in data[0], "Expected data to have a description"
        assert "view_count" in data[0], "Expected result to have a view count"
        assert "like_count" in data[0], "Expected result to have a like count"
        assert "favorite_count" in data[0], "Expected result to have a favorite count"
        assert "comment_count" in data[0], "Expected result to have a comment count"
        assert "thumbnails" in data[0], "Expected data to have thumbnails list"
        assert "transcript" in data[0], "Expected data to have a transcript"
        assert "published_at" in data[0], "Expected data to have a published_at"
    except Exception as e:
        assert False, "Expected data to be valid JSON"
        logger.error("Error loading JSON data from file: " + str(e))    

def test_get_nonexistent_file():
    test_files_dir = test_files_dir = os.path.join(Settings.project_root, Settings.test_files_dir)      
    storage = StorageFactory.get_storage("local", test_files_dir)
    try:
        data_str = storage.get("nonexistent_file.json")
        assert data_str is None, "Expected data to be None"
        logger.info("Retrieved test data from file")
    except FileNotFoundError as e:
        assert True, "Expected file not found error"
        logger.error("File not found error: " + str(e))


def test_delete():
    test_files_dir = test_files_dir = os.path.join(Settings.project_root, Settings.test_files_dir)      
    storage = StorageFactory.get_storage("local", test_files_dir)
    storage.delete("youtube-test-file-temp.json")
    logger.info("Deleted test data from file")


def test_iterate_and_process_items():
    test_files_dir = test_files_dir = os.path.join(Settings.project_root, Settings.test_files_dir)      
    storage = StorageFactory.get_storage("local", test_files_dir)

    storage.iterate_and_process_items(location=test_files_dir, filter_pattern="*.json", processor_func=lambda file: logger.info("Processing file: " + file))
    logger.info("Processed all files in storage")
