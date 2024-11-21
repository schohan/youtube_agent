import os
import pytest
from dotenv import load_dotenv
import sys

# Ensure the PYTHONPATH environment variable is set to the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from .env file
load_dotenv()

from app.research_agent.agent import get_youtube_videos

def test_get_youtube_videos():
    # Example test case for get_youtube_videos function
    search_term = "asthma treatments"
    results = get_youtube_videos(search_term)
    
    assert isinstance(results, list), "Expected a list of results"
    assert len(results) > 0, "Expected at least one result"
    assert "title" in results[0], "Expected result to have a title"
    assert "views" in results[0], "Expected result to have a view count"

if __name__ == "__main__":
    key = os.environ.get("YOUTUBE_API_KEY", "")
    print("KEY " + key)
    pytest.main()