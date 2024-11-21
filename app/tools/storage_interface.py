from abc import ABC, abstractmethod


class Storage(ABC):
    """
    Interface (abstract class) for storage i.e. file, database, cache etc
    """
    
    def __init__(self, **kwargs):
        pass

    @abstractmethod    
    def has_item(self, key):
        pass

    @abstractmethod    
    def get(self, key):
        pass
    
    @abstractmethod    
    def set(self, key, value):
        pass

    @abstractmethod    
    def delete(self, key):
        pass