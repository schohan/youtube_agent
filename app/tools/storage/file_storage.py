from app.tools.storage.storage_interface import Storage
from app.configs.app_config import Config
import os
import logging
from app.configs.logging_config import get_logger

class FileStorage(Storage):
    """
    File storage class. Implments the Storage interface for file storage either local or mounted. 
    Items are stored with the filename as key. 
    """
    type = "local"    
    logger = get_logger(__name__)

    def __init__(self, file_dir: str):        
        """
            Initialize the FileStorage class with the directory to store files.
            Args:
                directory (str): The directory to store files
        """
        self.directory = file_dir
        self.logger.info(f"Initializing FileStorage with directory {self.directory}")


        # initialize the storage directory using file system
        if not os.path.exists(self.directory):
            try:
                # Create the directory if it does not exist
                os.makedirs(self.directory)
            except OSError as e:
                # Raise an exception if the directory cannot be created
                raise Exception(f"Failed to create directory {self.directory}: {e}")
        
        # Raise an exception if the directory is not a directory
        if not os.path.isdir(self.directory):
            raise Exception(f"The path {self.directory} is not a directory") 

        self.logger.info(f"Initialized FileStorage with directory {self.directory}")


    # overrides the has_item method in the Storage class
    def has_item(self, key) -> bool:
        """
            Check if the file exists in the storage directory
            Args:
                key (str): The key to check
            Returns:
                bool: True if the file exists, False otherwise
        """
        return os.path.isfile(os.path.join(self.directory, key))
    
    # overrides the get method in the Storage class
    def get(self, key) -> str | None:
        """
            Get the contents of the file from the storage directory. 
            Note: The file is read as a string. For very large files, we will consider reading in chunks.
            
            Args:
                key (str): The key to get
            Returns:
                str | None: The contents of the file or None if the file does not exist
        """        
        file_path = os.path.join(self.directory, key)
        self.logger.info(f"Getting file {file_path} ")

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file {key} does not exist in the directory {self.directory}")
        
        with open(file_path, 'r') as file:
            return file.read()
    
    # overrides the set method in the Storage class
    def set(self, key, value):
        """
            Set the contents of the file in the storage directory.
            
            Args:
                key (str): The key to set
                value (str): The value to write to the file
        """
        file_path = os.path.join(self.directory, key)
        try:
            with open(file_path, 'w') as file:
                file.write(value)
        except OSError as e:
            raise Exception(f"Failed to write to file {file_path}: {e}")
  
    
    # overrides the delete method in the Storage class
    def delete(self, key):
        """
            Delete the file from the storage directory.
            
            Args:
                key (str): The key to delete
        """
        file_path = os.path.join(self.directory, key)
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            raise FileNotFoundError(f"The file {key} does not exist in the directory {self.directory}")