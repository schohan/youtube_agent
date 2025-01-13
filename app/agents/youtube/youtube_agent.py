from typing import final
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from app.agents.youtube.youtube_agent import search_youtube
from app.shared.content.youtube_search import YouTubeSearcher
from app.configs.settings import Settings
from datetime import datetime, timedelta
from app.agents.ontology.topic_ontology import TopicOntology
from app.shared.storage.storage_factory import StorageFactory
import logging

class YoutubeAgent:

    def __init__(self, storage_type: str = Settings.storage_type):
        self.storage_dir = Settings.raw_files_dir
        self.youtube_searcher = YouTubeSearcher(Settings.youtube_api_key)
        self.storage = StorageFactory.get_storage(storage_type, self.storage_dir)
        self.min_views = 1000
        self.min_comments = 100
        self.last_n_days = 30
        self.logger = logging.getLogger(__name__)

    async def download_youtube_videos(self, search_term: str, last_n_days: int = 30):
        """
        Get youtube videos based on a query

        Args:
            search_term (str): The query to search for
            last_n_days (int): The number of days to search for
        Returns:
            results (list): A list of dictionaries with video details
        """

        return await self.youtube_searcher.search_videos(search_term, 
                                                   max_results=Settings.max_youtube_results, 
                                                   min_views=self.min_views, 
                                                   min_comments=self.min_comments, 
                                                   published_after=datetime.now() - timedelta(days=self.last_n_days))

   

    async def download_youtube_videos_for_keywords(self, keywords: dict[str, str], last_n_days: int = 30):
        """
        Get youtube videos based on a list of keywords

        Args:
            keywords (dict[str, str]): A dictionary of keywords and their descriptions
            last_n_days (int): The number of days to search for

        Returns:
            results (list): A list of dictionaries with video details
        """
        for k,v in keywords.items():
           self.logger.info(f"Downloading videos for {k}")
           try:
               # check if the file exists
               if self.storage.get(f"{self.storage_dir}/videos_{k}.json"):
                   self.logger.info(f"File already exists for {k}")
                   continue
               
               videos = await self.download_youtube_videos(v, last_n_days)
               self.storage.set(  f"{self.storage_dir}/videos_{k}.json", videos)
           except Exception as e:
               self.logger.error(f"Error downloading videos for {k}: {e}")



    async def download_youtube_videos_for_ontology(self, ontology: TopicOntology, last_n_days: int = 30):
        """
        Get youtube videos based on a ontology
        
        Args:
            ontology (TopicOntology): The ontology to search for
            last_n_days (int): The number of days to search for

        Returns:
            results (list): A list of dictionaries with video details
        """
        keywords = ontology.get_keywords()
        await self.download_youtube_videos_for_keywords(keywords, last_n_days)