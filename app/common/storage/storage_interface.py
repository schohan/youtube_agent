from abc import ABC, abstractmethod

class Storage(ABC):
    """
    Interface (abstract class) for storage i.e. file, database, cache etc
    """
    

    @abstractmethod    
    def has_item(self, key) -> bool:
        """
            Check if the item exists in the storage
            Args:
                key (str): The key to check
            Returns:
                bool: True if the item exists, False otherwise
        """
        pass

    @abstractmethod    
    def get(self, key) -> str | None:
        """
            Get the item from the storage
            Args:
                key (str): The key to get
            Returns:
                str | None: The value of the key or None if the key does not exist
        """
        pass
    
    @abstractmethod    
    def set(self, key, value):
        """
            Set the item in the storage
            Args:
                key (str): The key to set
                value (str): The value to set
        """
        pass

    @abstractmethod    
    def delete(self, key):
        """
            Delete the item from the storage
            Args:
                key (str): The key to delete
        """
        pass

    @abstractmethod
    def iterate_and_process_items(self, location, filter_pattern, processor_func):
        """
            Iterate over all items in the storage and process them
            Args:
                location (str): The location to iterate over
                filter_pattern (str): The filter pattern to select items. e.g. *.txt
                processor_func (function): The function to process each item
        """
        pass    