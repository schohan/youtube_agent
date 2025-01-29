import os
from dotenv import load_dotenv
import sys
from app.common.content.content_summarizer import ContentSummarizer
from app.configs.settings import Settings
from app.configs.logging_config import get_logger
from app.common.storage.file_storage import FileStorage
from app.common.storage.storage_interface import Storage
from app.common.storage.storage_factory import StorageFactory
from app.common.data_converters.json_helper import JsonHelper
from app.common.llm.llm_factory import LLMFactory
from typing import Literal
# Create a logger
logger = get_logger(__name__)


def test_summarize_content(return_format: Literal["json", "markdown", "html", "text"] = "json"):
    llm = LLMFactory.get_llm(Settings.summarizer_llm)
    content_summarizer = ContentSummarizer(llm)
    test_files_dir = test_files_dir = os.path.join(Settings.project_root, Settings.test_files_dir)      
    storage = StorageFactory.get_storage("local", test_files_dir)
   
    raw_text = storage.get("transcript.txt")
    assert raw_text is not None, "Raw text is None"
    summary = content_summarizer.summarize_content(raw_text, return_format)
    print(summary)
    return summary


