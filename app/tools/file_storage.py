from app.tools.storage_interface import Storage


class FileStorage(Storage):
    """
    File storage class. Implments the Storage interface for file storage either local or mounted. 
    """
    
    def __init__(self, **kwargs):
        pass
    
    def has_item(self, key):
        pass
    
    def get(self, key):
        pass
    
    def set(self, key, value):
        pass
    
    def delete(self, key):
        pass