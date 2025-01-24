import pytest
import os
from dotenv import load_dotenv
import sys
from app.configs.logging_config import get_logger
from app.configs.settings import Settings
from app.agents.ontology.topic_ontology import TopicNode, TopicOntology
import json
from app.common.storage.storage_factory import StorageFactory
from app.common.storage.file_storage import FileStorage

# Ensure the PYTHONPATH environment variable is set to the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

# Create a logger
logger = get_logger(__name__)

# Load environment variables from .env file
load_dotenv()

# setup tests
storage = StorageFactory.get_storage(Settings.storage_type, Settings.test_files_dir)


def test_researched_ontology():
    """
    Test to convert a keyword object in string format to a proper JSON object. 
    """
    ontology = [TopicNode(title='Health', children=[TopicNode(title='Physical Health', children=[TopicNode(title='Exercise', children=[TopicNode(title='Cardiovascular', children=[]), TopicNode(title='Strength Training', children=[]), TopicNode(title='Flexibility', children=[])]), TopicNode(title='Nutrition', children=[TopicNode(title='Balanced Diet', children=[]), TopicNode(title='Hydration', children=[]), TopicNode(title='Vitamins and Minerals', children=[])]), TopicNode(title='Sleep', children=[TopicNode(title='Sleep Hygiene', children=[]), TopicNode(title='Sleep Disorders', children=[])]), TopicNode(title='Preventive Care', children=[TopicNode(title='Vaccinations', children=[]), TopicNode(title='Regular Check-ups', children=[])])]), TopicNode(title='Mental Health', children=[TopicNode(title='Stress Management', children=[TopicNode(title='Mindfulness', children=[]), TopicNode(title='Meditation', children=[])]), TopicNode(title='Mental Disorders', children=[TopicNode(title='Anxiety', children=[]), TopicNode(title='Depression', children=[])]), TopicNode(title='Therapies', children=[TopicNode(title='Cognitive Behavioral Therapy', children=[]), TopicNode(title='Psychotherapy', children=[])])]), TopicNode(title='Social Health', children=[TopicNode(title='Relationships', children=[TopicNode(title='Family', children=[]), TopicNode(title='Friendships', children=[])]), TopicNode(title='Community Engagement', children=[TopicNode(title='Volunteering', children=[]), TopicNode(title='Social Activities', children=[])])]), TopicNode(title='Environmental Health', children=[TopicNode(title='Pollution', children=[TopicNode(title='Air Quality', children=[]), TopicNode(title='Water Quality', children=[])]), TopicNode(title='Sustainability', children=[TopicNode(title='Recycling', children=[]), TopicNode(title='Conservation', children=[])])]), TopicNode(title='Occupational Health', children=[TopicNode(title='Work-Life Balance', children=[TopicNode(title='Time Management', children=[]), TopicNode(title='Stress Reduction', children=[])]), TopicNode(title='Workplace Safety', children=[TopicNode(title='Ergonomics', children=[]), TopicNode(title='Hazard Prevention', children=[])])])])]
    ontology_json = json.dumps([keyword.to_dict() for keyword in ontology], indent=3)
    
    assert ontology_json is not None and "Sleep Hygiene" in ontology_json
    assert ontology_json is not None and "Environmental Health" in ontology_json
    

def test_mind_map():
    """
    Test to convert a keyword object in string format to a proper JSON object. 
    """
    map = [TopicNode(title='Physical Health', children=[TopicNode(title='Nutrition', children=[TopicNode(title='Balanced Diet', children=[]), TopicNode(title='Macronutrients', children=[]), TopicNode(title='Micronutrients', children=[]), TopicNode(title='Hydration', children=[])]), TopicNode(title='Exercise', children=[TopicNode(title='Cardiovascular Fitness', children=[]), TopicNode(title='Strength Training', children=[]), TopicNode(title='Flexibility', children=[]), TopicNode(title='Endurance', children=[])]), TopicNode(title='Sleep', children=[TopicNode(title='Sleep Cycles', children=[]), TopicNode(title='Sleep Hygiene', children=[]), TopicNode(title='Sleep Disorders', children=[])]), TopicNode(title='Preventive Care', children=[TopicNode(title='Vaccinations', children=[]), TopicNode(title='Regular Check-ups', children=[]), TopicNode(title='Screenings', children=[])])]), TopicNode(title='Mental Health', children=[TopicNode(title='Emotional Well-being', children=[TopicNode(title='Stress Management', children=[]), TopicNode(title='Emotional Intelligence', children=[]), TopicNode(title='Mindfulness', children=[])]), TopicNode(title='Mental Disorders', children=[TopicNode(title='Anxiety Disorders', children=[]), TopicNode(title='Depression', children=[]), TopicNode(title='Bipolar Disorder', children=[]), TopicNode(title='Schizophrenia', children=[])]), TopicNode(title='Therapies', children=[TopicNode(title='Cognitive Behavioral Therapy', children=[]), TopicNode(title='Psychotherapy', children=[]), TopicNode(title='Medication', children=[])])]), TopicNode(title='Social Health', children=[TopicNode(title='Relationships', children=[TopicNode(title='Family', children=[]), TopicNode(title='Friendships', children=[]), TopicNode(title='Romantic Relationships', children=[])]), TopicNode(title='Community Engagement', children=[TopicNode(title='Volunteering', children=[]), TopicNode(title='Social Support Networks', children=[])]), TopicNode(title='Communication Skills', children=[TopicNode(title='Active Listening', children=[]), TopicNode(title='Conflict Resolution', children=[]), TopicNode(title='Empathy', children=[])])]), TopicNode(title='Environmental Health', children=[TopicNode(title='Pollution', children=[TopicNode(title='Air Quality', children=[]), TopicNode(title='Water Quality', children=[]), TopicNode(title='Soil Contamination', children=[])]), TopicNode(title='Sustainability', children=[TopicNode(title='Recycling', children=[]), TopicNode(title='Renewable Energy', children=[]), TopicNode(title='Conservation', children=[])]), TopicNode(title='Occupational Health', children=[TopicNode(title='Workplace Safety', children=[]), TopicNode(title='Ergonomics', children=[]), TopicNode(title='Work-Life Balance', children=[])])])]
    
    map_json = json.dumps([node.to_dict() for node in map], indent=3)

    print(f"Map==>> {map_json}")

    assert "Sleep Hygiene" in map_json
    assert "Physical Health" in map_json
    assert "Mental Health" in map_json
    assert "Social Health" in map_json
    assert "Environmental Health" in map_json


def test_load_curriculum_ontology_basic_structure():
    """Test that the loaded curriculum ontology has the correct basic structure"""
    ontology_file = 'health-ontology.json'
    ontology_json = storage.get(ontology_file)
    curriculum_data = TopicOntology.load_ontology(ontology_json)
    
    assert curriculum_data is not None
    assert isinstance(curriculum_data, TopicOntology)
    assert hasattr(curriculum_data, 'title')
    assert hasattr(curriculum_data, 'topics')
    assert curriculum_data.title == "Health"

def test_load_curriculum_ontology_first_level_categories():
    """Test that all expected top-level categories exist in the curriculum"""
    ontology_file = 'health-ontology.json'
    ontology_json = storage.get(ontology_file)
    curriculum_data = TopicOntology.load_ontology(ontology_json)
    
    assert curriculum_data is not None
    first_level = {child.title for child in curriculum_data.topics}
    expected_categories = {
        "Physical Health",
        "Mental Health", 
        "Social Health",
        "Environmental Health",
        "Occupational Health"
    }
    assert first_level == expected_categories

def test_load_curriculum_ontology_nested_structure():
    """Test that the nested structure contains expected child topics"""
    ontology_file = 'health-ontology.json'
    ontology_json = storage.get(ontology_file)
    curriculum_data = TopicOntology.load_ontology(ontology_json)
    
    assert curriculum_data is not None

    # Test Physical Health branch
    physical_health = next(child for child in curriculum_data.topics 
                         if child.title == "Physical Health")
    physical_health_topics = {child.title for child in physical_health.children}
    assert "Exercise" in physical_health_topics
    
    # Test Mental Health branch
    mental_health = next(child for child in curriculum_data.topics
                        if child.title == "Mental Health")
    mental_health_topics = {child.title for child in mental_health.children}
    assert "Stress Management" in mental_health_topics

def test_load_curriculum_ontology_first_level_categories2():
    """Test that all expected top-level categories exist in the curriculum"""
    ontology_file = 'health-ontology.json'
    ontology_json = storage.get(ontology_file)
    curriculum_data = TopicOntology.load_ontology(ontology_json)
    
    
    assert curriculum_data is not None
    first_level = {child.title for child in curriculum_data.topics}
    expected_categories = {
        "Physical Health",
        "Mental Health", 
        "Social Health",
        "Environmental Health",
        "Occupational Health"
    }
    assert first_level == expected_categories

def test_get_keywords():
    ontology_file = 'health-ontology.json'
    ontology_json = storage.get(ontology_file)
    curriculum_data = TopicOntology.load_ontology(ontology_json)
    assert curriculum_data is not None

    keywords = curriculum_data.get_keywords("health")
    #print(f"Keywords==>> {keywords}")
    assert keywords is not None
    assert "health-physical health-exercise-cardiovascular" in keywords
    assert "health-physical health-exercise-strength training" in keywords
    assert "health-physical health-exercise-flexibility" in keywords
