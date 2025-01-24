from logging import getLogger

from sqlalchemy import exists
from app.common.storage.storage_interface import Storage
from app.configs.settings import Settings
import os
from app.configs.logging_config import get_logger
from pathlib import Path

class FileStorage(Storage):
    """
    File storage class. Implments the Storage interface to act on files stored in local/mounted file storage. 
    Items are stored with the filename as key. 
    """

    def __init__(self, file_dir: str):        
        """
            Initialize the FileStorage class with the directory to store files.
            Args:
                directory (str): The directory to store files
        """
        self.logger = getLogger(__name__)
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

        if not self.has_item(key):
            raise FileNotFoundError(f"The file {key} does not exist in the directory {self.directory}")
        
        with open(file_path, 'r') as file:
            return file.read()
    


    # overrides the set method in the Storage class
    def set(self, key: str, value: str):
        """
            Set the contents of the file in the storage directory.
            
            Args:
                key (str): The key to set
                value (str): The value to write to the file
        """
        file_path = os.path.join(self.directory, key)
        self.logger.info(f"Saving contents to file {file_path} ")
        
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
        
    
    # overrides the iterate_and_process_items method in the Storage class    
    def iterate_and_process_items(self, location=".",  filter_pattern="*", processor_func=lambda x: print(x)):
        """
            Iterate over all files in the storage directory and process them.
            This is a placeholder method and should be implemented based on the processing logic.
            Args:
                processor_func (function): The function to process the file
                directory (str): The directory to iterate over
                file_filter (str): The file filter to apply
            Returns:
                None
        """
        directory_path = Path(location)
        self.logger.info(" --- > Iterating over directory_path " + directory_path.name + " with filter " + filter_pattern)

        for file in directory_path.rglob(filter_pattern):
            if file.is_file():   # Check if it's a file
                self.logger.info(f"Found file: {file.name}")
                
                # Process the file (e.g., read or modify it)
                with file.open('r') as f:
                    content = f.read()
                    processor_func(content)  
    

##########################
#  EXAMPLE USAGE 
##########################

if __name__ == "__main__":
    storage = FileStorage("data/raw")
    print(storage.has_item("test.txt"))
    storage.set("test.txt", "Hello, World!")
    print(storage.get("test.txt"))
    # storage.delete("test.txt")
    # print(storage.has_item("test.txt"))