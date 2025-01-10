from app.shared.storage.storage_interface import Storage
from app.configs.settings import Settings
from app.configs.logging_config import get_logger

class S3Storage(Storage):
    """
    S3 storage class. Implments the Storage interface for file storage either local or mounted. 
    """
    type = "s3"
    logger = get_logger(__name__)

    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.logger = get_logger(__name__)
    
    def has_item(self, key) -> bool:
        self.logger.info(f"Checking if item with key {key} exists in S3 storage. TO BE IMPLEMENTED")
        return False  # Placeholder return value
    
    def get(self, key):
        self.logger.info(f"Getting item with key {key} from S3 storage. TO BE IMPLEMENTED")
        pass
    
    def set(self, key, value):
        self.logger.info(f"Setting item with key {key} in S3 storage. TO BE IMPLEMENTED")
        pass
    
    def delete(self, key):
        self.logger.info(f"Deleting item with key {key} from S3 storage. TO BE IMPLEMENTED")
        pass

    def iterate_and_process_items(self, location, filter_pattern, processor_func):
        self.logger.info(f"Iterating over items in S3 storage with location {location} and filter pattern {filter_pattern}. TO BE IMPLEMENTED")
        pass