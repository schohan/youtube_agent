from attr import dataclass
from app.shared.data_converters.json_helper import JsonHelper
from app.configs.logging_config import get_logger
import json
logger = get_logger(__name__)

@dataclass
class Person:
    name: str
    age: int
    city: str

def test_json_to_list():
    logger.info("Running test_json_to_list")
    json_str = '[{"name": "John", "age": 30, "city": "New York"}, {"name": "Jane", "age": 25, "city": "Chicago"}]'
    data_class = type("Person", (), {})
    result = JsonHelper.json_to_list(json_str, Person)

    logger.info("After conversion to list -->>> " + str(result))
    assert type(result) == list
    assert type(result[0]) == Person
    assert type(result[1]) == Person
    assert result[0].name == "John"
    assert result[0].age == 30
    assert result[0].city == "New York"


def test_list_to_json():
    logger.info("Running test_list_to_json")
    data = [Person("John", 30, "New York"), Person("Jane", 25, "Chicago")]
    result = JsonHelper.list_to_json(data)
    logger.info("After conversion to String -->>> " + result)
    assert type(result) == str
    assert result == '[{"name": "John", "age": 30, "city": "New York"}, {"name": "Jane", "age": 25, "city": "Chicago"}]'


def test_to_json():
    logger.info("Running test_to_json")
    # load data/raw/videos_single_record.json
    with open('data/raw/videos_single_record.json', 'r') as file:
        videos = json.load(file)

        for video in videos:
            # Convert any datetime strings to datetime objects and back for testing
            if 'published_at' in video:
                video['published_at'] = video['published_at'].isoformat() if hasattr(video['published_at'], 'isoformat') else video['published_at']
            
            print(video)
            result = JsonHelper.to_json(video)
            logger.info("After conversion to String -->>> " + result)
            assert type(result) == str
        
