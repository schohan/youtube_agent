from dataclasses import dataclass
from dotenv import load_dotenv
import os

import openai

#load env variables from .evn file
load_dotenv()

@dataclass
class Config:
    """
    Base configuration class. Contains configuration settings
    """

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    
    #llms, models and properties
    llm_openai="openai"
    llm_ollama = "ollama"
    llm_claude = "claude"

    openai_model_name = os.environ.get("MODEL_NAME", "gpt-4o") 
    openai_model_temperature = float(os.environ.get("MODEL_TEMPERATURE", 0.1))

    # api keys and related props  
    openai_api_key = os.environ.get("OPENAI_API_KEY", "")
    claude_api_key = os.environ.get("CLAUDE_API_KEY", "")
    tavily_api_key = os.environ.get("TAVILY_API_KEY", "")
    youtube_api_key = os.environ.get("YOUTUBE_API_KEY", "")
    max_youtube_results = int(os.environ.get("MAX_YOUTUBE_RESULTS", 10))
    
    # storage
    storage_type = os.environ.get("STORAGE_TYPE", "local")
    raw_files_dir = os.environ.get("RAW_FILES_DIR", "data/raw")
    processed_files_dir = os.environ.get("PROCESSED_FILES_DIR", "data/processed")
    test_files_dir = os.environ.get("TEST_FILES_DIR", "data/test")
    model_files_dir = os.environ.get("MODEL_FILES_DIR", "data/models")

    use_test_data = os.environ.get("USE_TEST_DATA", True)

    # local_llm_url = os.environ.get("LOCAL_LLM_URL", "http://localhost:8000")
