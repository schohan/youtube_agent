from app.tools.storage.storage_interface import Storage
from app.configs.app_config import Config

class S3Storage(Storage):
    """
    S3 storage class. Implments the Storage interface for file storage either local or mounted. 
    """
    type = "s3"

    def __init__(self, bucket_name: str):
        pass
    
    def has_item(self, key) -> bool:
        # Implement the logic to check if the item exists in S3 storage
        return False  # Placeholder return value
    
    def get(self, key):
        pass
    
    def set(self, key, value):
        pass
    
    def delete(self, key):
        pass