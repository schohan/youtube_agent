import json
from dataclasses import asdict

class JsonHelper:
    
    @staticmethod
    def json_to_list(json_list_str: str, data_class):
        """
        Convert a string to a JSON object
        Args:
            json_str (str): The string to convert
            data_class (class): The class to convert the JSON object to
        Returns:
            list: The list of JSON objects
        """
        return [data_class(**item) for item in json.loads(json_list_str)]
    

    @staticmethod
    def list_to_json(json_data_list: list):
        """
        Convert a JSON object to a string
        Args:
            json_data (dict): The JSON object to convert
        Returns:
            str: The JSON object as a string
        """
        dict_list = [data.__dict__ for data in json_data_list]
        return json.dumps(dict_list)
    

    

    @staticmethod
    def to_json(json_data):
        """
        Convert a JSON object to a string
        Args:
            json_data (dict): The JSON object to convert
        Returns:
            str: The JSON object as a string
        """
        #return json.dumps(asdict(json_data))
        return json.dumps(json_data)
    
    @staticmethod
    def load_json(json_str):
        """
        Convert a string to a JSON object
        Args:
            json_str (str): The string to convert
        Returns:
            dict: The string as a JSON object
        """
        return json.loads(json_str)