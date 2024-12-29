import os
from app.toolhelpers.storage.file_storage import FileStorage
from app.toolhelpers.storage.s3_storage import S3Storage
from app.configs.settings import Config

class StorageFactory:
    """
    Factory class to get storage instance based on storage type
    """
    @staticmethod
    def get_storage(storage_type: str, root_location: str) -> FileStorage | S3Storage:
        """
        Factory method to get storage instance based on storage type
        Args:
            storage_type (str): The type of storage to use. e.g. local, s3
        Returns:
            storage (Storage): An instance of the storage class            
        """

        if storage_type == "local":            
            return FileStorage(root_location)
        elif storage_type == "s3":
            return S3Storage(root_location)
        else:
            raise ValueError("Invalid storage type")