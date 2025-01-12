import pytest
import os
from dotenv import load_dotenv
import sys
from app.configs.logging_config import get_logger
from app.configs.settings import Settings
from app.agents.ontology.topic_ontology import TopicNode, TopicOntology
import json

# Ensure the PYTHONPATH environment variable is set to the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

# Create a logger
logger = get_logger(__name__)

# Load environment variables from .env file
load_dotenv()


def test_researched_ontology():
    """
    Test to convert a keyword object in string format to a proper JSON object. 
    """
    ontology = [TopicNode(title='Health', children=[TopicNode(title='Physical Health', children=[TopicNode(title='Exercise', children=[TopicNode(title='Cardiovascular', children=None), TopicNode(title='Strength Training', children=None), TopicNode(title='Flexibility', children=None)]), TopicNode(title='Nutrition', children=[TopicNode(title='Balanced Diet', children=None), TopicNode(title='Hydration', children=None), TopicNode(title='Vitamins and Minerals', children=None)]), TopicNode(title='Sleep', children=[TopicNode(title='Sleep Hygiene', children=None), TopicNode(title='Sleep Disorders', children=None)]), TopicNode(title='Preventive Care', children=[TopicNode(title='Vaccinations', children=None), TopicNode(title='Regular Check-ups', children=None)])]), TopicNode(title='Mental Health', children=[TopicNode(title='Stress Management', children=[TopicNode(title='Mindfulness', children=None), TopicNode(title='Meditation', children=None)]), TopicNode(title='Mental Disorders', children=[TopicNode(title='Anxiety', children=None), TopicNode(title='Depression', children=None)]), TopicNode(title='Therapies', children=[TopicNode(title='Cognitive Behavioral Therapy', children=None), TopicNode(title='Psychotherapy', children=None)])]), TopicNode(title='Social Health', children=[TopicNode(title='Relationships', children=[TopicNode(title='Family', children=None), TopicNode(title='Friendships', children=None)]), TopicNode(title='Community Engagement', children=[TopicNode(title='Volunteering', children=None), TopicNode(title='Social Activities', children=None)])]), TopicNode(title='Environmental Health', children=[TopicNode(title='Pollution', children=[TopicNode(title='Air Quality', children=None), TopicNode(title='Water Quality', children=None)]), TopicNode(title='Sustainability', children=[TopicNode(title='Recycling', children=None), TopicNode(title='Conservation', children=None)])]), TopicNode(title='Occupational Health', children=[TopicNode(title='Work-Life Balance', children=[TopicNode(title='Time Management', children=None), TopicNode(title='Stress Reduction', children=None)]), TopicNode(title='Workplace Safety', children=[TopicNode(title='Ergonomics', children=None), TopicNode(title='Hazard Prevention', children=None)])])])]
    ontology_json = json.dumps([keyword.to_dict() for keyword in ontology], indent=3)
    
    assert ontology_json is not None and "Sleep Hygiene" in ontology_json
    assert ontology_json is not None and "Environmental Health" in ontology_json
    

def test_mind_map():
    """
    Test to convert a keyword object in string format to a proper JSON object. 
    """
    map = [TopicNode(title='Physical Health', children=[TopicNode(title='Nutrition', children=[TopicNode(title='Balanced Diet', children=None), TopicNode(title='Macronutrients', children=None), TopicNode(title='Micronutrients', children=None), TopicNode(title='Hydration', children=None)]), TopicNode(title='Exercise', children=[TopicNode(title='Cardiovascular Fitness', children=None), TopicNode(title='Strength Training', children=None), TopicNode(title='Flexibility', children=None), TopicNode(title='Endurance', children=None)]), TopicNode(title='Sleep', children=[TopicNode(title='Sleep Cycles', children=None), TopicNode(title='Sleep Hygiene', children=None), TopicNode(title='Sleep Disorders', children=None)]), TopicNode(title='Preventive Care', children=[TopicNode(title='Vaccinations', children=None), TopicNode(title='Regular Check-ups', children=None), TopicNode(title='Screenings', children=None)])]), TopicNode(title='Mental Health', children=[TopicNode(title='Emotional Well-being', children=[TopicNode(title='Stress Management', children=None), TopicNode(title='Emotional Intelligence', children=None), TopicNode(title='Mindfulness', children=None)]), TopicNode(title='Mental Disorders', children=[TopicNode(title='Anxiety Disorders', children=None), TopicNode(title='Depression', children=None), TopicNode(title='Bipolar Disorder', children=None), TopicNode(title='Schizophrenia', children=None)]), TopicNode(title='Therapies', children=[TopicNode(title='Cognitive Behavioral Therapy', children=None), TopicNode(title='Psychotherapy', children=None), TopicNode(title='Medication', children=None)])]), TopicNode(title='Social Health', children=[TopicNode(title='Relationships', children=[TopicNode(title='Family', children=None), TopicNode(title='Friendships', children=None), TopicNode(title='Romantic Relationships', children=None)]), TopicNode(title='Community Engagement', children=[TopicNode(title='Volunteering', children=None), TopicNode(title='Social Support Networks', children=None)]), TopicNode(title='Communication Skills', children=[TopicNode(title='Active Listening', children=None), TopicNode(title='Conflict Resolution', children=None), TopicNode(title='Empathy', children=None)])]), TopicNode(title='Environmental Health', children=[TopicNode(title='Pollution', children=[TopicNode(title='Air Quality', children=None), TopicNode(title='Water Quality', children=None), TopicNode(title='Soil Contamination', children=None)]), TopicNode(title='Sustainability', children=[TopicNode(title='Recycling', children=None), TopicNode(title='Renewable Energy', children=None), TopicNode(title='Conservation', children=None)]), TopicNode(title='Occupational Health', children=[TopicNode(title='Workplace Safety', children=None), TopicNode(title='Ergonomics', children=None), TopicNode(title='Work-Life Balance', children=None)])])]
    
    map_json = json.dumps([node.to_dict() for node in map], indent=3)

    print(f"Map==>> {map_json}")

    assert "Sleep Hygiene" in map_json
    assert "Physical Health" in map_json
    assert "Mental Health" in map_json
    assert "Social Health" in map_json
    assert "Environmental Health" in map_json


def test_load_curriculum_ontology():
    """
    Test loading and validating curriculum ontology from JSON file
    """
    # Load JSON file
    
    curriculum_data = TopicOntology.load_ontology('data/test/curriculum-ontology.json')
    # Basic structure validation
    assert isinstance(curriculum_data, TopicOntology)
    assert hasattr(curriculum_data, 'title')
    assert hasattr(curriculum_data, 'topics')
    assert curriculum_data.title == "Health"
    
    # Validate first level categories exist
    first_level = [child.title for child in curriculum_data.topics]
    expected_categories = [
        "Physical Health",
        "Mental Health", 
        "Social Health",
        "Environmental Health",
        "Occupational Health"
    ]
    assert all(category in first_level for category in expected_categories)
    
    # Validate some nested structures
    physical_health = next(child for child in curriculum_data.topics 
                         if child.title == "Physical Health")
    assert physical_health.children is not None and "Exercise" in [child.title for child in physical_health.children]
    
    mental_health = next(child for child in curriculum_data.topics
                        if child.title == "Mental Health")
    assert mental_health.children is not None and "Stress Management" in [child.title for child in mental_health.children]
