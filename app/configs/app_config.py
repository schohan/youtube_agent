from dataclasses import dataclass
from dotenv import load_dotenv
import os

#load env variables from .evn file
load_dotenv()

class Config:
    """
    Base configuration class. Contains configuration settings
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    youtube_api_key = os.environ.get("YOUTUBE_API_KEY", "")
    max_youtube_results = int(os.environ.get("MAX_YOUTUBE_RESULTS", 10))
    
    open_api_key = os.environ.get("OPENAI_API_KEY", "")
    tavily_api_key = os.environ.get("TAVILY_API_KEY", "")
    
    raw_files_dir = os.environ.get("RAW_FILES_DIR", "data/raw")
    processed_files_dir = os.environ.get("PROCESSED_FILES_DIR", "data/processed")
    test_files_dir = os.environ.get("TEST_FILES_DIR", "data/test")
    model_files_dir = os.environ.get("MODEL_FILES_DIR", "data/models")