from calendar import c
from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv
import os

import openai

#load env variables from .evn file
load_dotenv(override=True)

@dataclass
class Settings:
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
    openai_max_tokens = int(os.environ.get("MODEL_MAX_TOKENS", 1000))
    openai_top_p = float(os.environ.get("MODEL_TOP_P", 1.0))

    claude_api_key = os.environ.get("CLAUDE_API_KEY", "")
    claude_url = os.environ.get("CLAUDE_URL", "")
    claude_model_name = os.environ.get("CLAUDE_MODEL_NAME", "claude=3.5")

    # api keys and related props  
    openai_api_key = os.environ.get("OPENAI_API_KEY", "")
    tavily_api_key = os.environ.get("TAVILY_API_KEY", "")

    # ontology related props
    ontology_llm = llm_openai

    # youtube related props
    youtube_api_key = os.environ.get("YOUTUBE_API_KEY", "")
    youtube_max_results = int(os.environ.get("YOUTUBE_MAX_RESULTS", 10))
    youtube_min_views = int(os.environ.get("YOUTUBE_MIN_VIEWS", 1000))
    youtube_min_comments = int(os.environ.get("YOUTUBE_MIN_COMMENTS", 10))
    youtube_last_n_days = int(os.environ.get("YOUTUBE_LAST_N_DAYS", 365))
    youtube_overwrite_files = os.environ.get("YOUTUBE_OVERWRITE_FILES", "True") == "True"

    # storage
    storage_type = os.environ.get("STORAGE_TYPE", "local")
    raw_files_dir = os.environ.get("RAW_FILES_DIR", "data/raw")
    processed_files_dir = os.environ.get("PROCESSED_FILES_DIR", "data/processed")
    test_files_dir = os.environ.get("TEST_FILES_DIR", "data/test")
    model_files_dir = os.environ.get("MODEL_FILES_DIR", "data/models")

    use_test_data: bool = os.environ.get("USE_TEST_DATA", "True") == "True"

    # YouTube settings
    min_youtube_views: int = 1000
    min_youtube_comments: int = 10
    max_youtube_results: int = 10
    youtube_last_n_days: int = 365

