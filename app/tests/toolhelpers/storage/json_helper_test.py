from attr import dataclass
from app.shared.data_converters.json_helper import JsonHelper
from app.configs.logging_config import get_logger

logger = get_logger(__name__)

@dataclass
class Person:
    name: str
    age: int
    city: str

def test_str_to_list():
    logger.info("Running test_str_to_list")
    json_str = '[{"name": "John", "age": 30, "city": "New York"}, {"name": "Jane", "age": 25, "city": "Chicago"}]'
    data_class = type("Person", (), {})
    result = JsonHelper.str_to_list(json_str, Person)

    logger.info("After conversion to list -->>> " + str(result))
    assert type(result) == list
    assert type(result[0]) == Person
    assert type(result[1]) == Person
    assert result[0].name == "John"
    assert result[0].age == 30
    assert result[0].city == "New York"


def test_list_to_str():
    logger.info("Running test_list_to_str")
    data = [Person("John", 30, "New York"), Person("Jane", 25, "Chicago")]
    result = JsonHelper.list_to_str(data)
    logger.info("After conversion to String -->>> " + result)
    assert type(result) == str
    assert result == '[{"name": "John", "age": 30, "city": "New York"}, {"name": "Jane", "age": 25, "city": "Chicago"}]'

