import pytest
import os
from dotenv import load_dotenv
import sys
from app.configs.logging_config import get_logger
from app.configs.settings import Settings
from app.agents.keywords.researched_state import MindMapNode
import json

# Ensure the PYTHONPATH environment variable is set to the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

# Create a logger
logger = get_logger(__name__)

# Load environment variables from .env file
load_dotenv()


def test_researched_keywords():
    """
    Test to convert a keyword object in string format to a proper JSON object. 
    """
    keywords = [MindMapNode(title='Health', children=[MindMapNode(title='Physical Health', children=[MindMapNode(title='Exercise', children=[MindMapNode(title='Cardiovascular', children=None), MindMapNode(title='Strength Training', children=None), MindMapNode(title='Flexibility', children=None)]), MindMapNode(title='Nutrition', children=[MindMapNode(title='Balanced Diet', children=None), MindMapNode(title='Hydration', children=None), MindMapNode(title='Vitamins and Minerals', children=None)]), MindMapNode(title='Sleep', children=[MindMapNode(title='Sleep Hygiene', children=None), MindMapNode(title='Sleep Disorders', children=None)]), MindMapNode(title='Preventive Care', children=[MindMapNode(title='Vaccinations', children=None), MindMapNode(title='Regular Check-ups', children=None)])]), MindMapNode(title='Mental Health', children=[MindMapNode(title='Stress Management', children=[MindMapNode(title='Mindfulness', children=None), MindMapNode(title='Meditation', children=None)]), MindMapNode(title='Mental Disorders', children=[MindMapNode(title='Anxiety', children=None), MindMapNode(title='Depression', children=None)]), MindMapNode(title='Therapies', children=[MindMapNode(title='Cognitive Behavioral Therapy', children=None), MindMapNode(title='Psychotherapy', children=None)])]), MindMapNode(title='Social Health', children=[MindMapNode(title='Relationships', children=[MindMapNode(title='Family', children=None), MindMapNode(title='Friendships', children=None)]), MindMapNode(title='Community Engagement', children=[MindMapNode(title='Volunteering', children=None), MindMapNode(title='Social Activities', children=None)])]), MindMapNode(title='Environmental Health', children=[MindMapNode(title='Pollution', children=[MindMapNode(title='Air Quality', children=None), MindMapNode(title='Water Quality', children=None)]), MindMapNode(title='Sustainability', children=[MindMapNode(title='Recycling', children=None), MindMapNode(title='Conservation', children=None)])]), MindMapNode(title='Occupational Health', children=[MindMapNode(title='Work-Life Balance', children=[MindMapNode(title='Time Management', children=None), MindMapNode(title='Stress Reduction', children=None)]), MindMapNode(title='Workplace Safety', children=[MindMapNode(title='Ergonomics', children=None), MindMapNode(title='Hazard Prevention', children=None)])])])]
    keywords_json = json.dumps([keyword.to_dict() for keyword in keywords], indent=3)
    
    #print(f"Keywords==>> {keywords_json}")
    #logger.info(f"Keywords==>> {keywords_json}")

    assert "Sleep Hygiene" in keywords_json
    assert "Environmental Health" in keywords_json
    


def test_load_curriculum_keywords():
    """
    Test loading and validating curriculum keywords from JSON file
    """
    # Load JSON file
    with open('data/test/curriculum-keywords.json', 'r') as f:
        curriculum_data = json.load(f)
    
    # Basic structure validation
    assert isinstance(curriculum_data, dict)
    assert "title" in curriculum_data
    assert "children" in curriculum_data
    assert curriculum_data["title"] == "Health"
    
    # Validate first level categories exist
    first_level = [child["title"] for child in curriculum_data["children"]]
    expected_categories = [
        "Physical Health",
        "Mental Health", 
        "Social Health",
        "Environmental Health",
        "Occupational Health"
    ]
    assert all(category in first_level for category in expected_categories)
    
    # Validate some nested structures
    physical_health = next(child for child in curriculum_data["children"] 
                            if child["title"] == "Physical Health")
    assert "Exercise" in [child["title"] for child in physical_health["children"]]
    
    mental_health = next(child for child in curriculum_data["children"]
                        if child["title"] == "Mental Health")
    assert "Stress Management" in [child["title"] for child in mental_health["children"]]
