from typing import final
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from app.shared.content.youtube_search import YouTubeSearcher
from app.configs.settings import Settings
from datetime import datetime, timedelta
from app.agents.ontology.topic_ontology import TopicOntology
from app.shared.data_converters.json_helper import JsonHelper
from app.shared.storage.storage_factory import StorageFactory
import logging
from app.shared.content.youtube_search import VideoStats
from tenacity import retry, stop_after_delay, stop_after_attempt, wait_exponential
import asyncio


class YoutubeAgent:

    def __init__(self, storage_type: str = Settings.storage_type):
        self.storage_dir = Settings.raw_files_dir
        self.youtube_searcher = YouTubeSearcher(Settings.youtube_api_key)
        self.storage = StorageFactory.get_storage(storage_type, self.storage_dir)
        self.min_views = Settings.youtube_min_views
        self.min_comments = Settings.youtube_min_comments
        self.last_n_days = Settings.youtube_last_n_days
        self.logger = logging.getLogger(__name__)


    @retry(stop=(stop_after_delay(10) | stop_after_attempt(3)), wait=wait_exponential(multiplier=1, min=4, max=15))
    async def download_youtube_videos(self, search_term: str) -> list[VideoStats]:
        """
        Get youtube videos based on a query

        Args:
            search_term (str): The query to search for
            last_n_days (int): The number of days to search for
        Returns:
            results (list): A list of dictionaries with video details
        """

        return await self.youtube_searcher.search_videos(search_term, 
                                                   max_results=Settings.youtube_max_results, 
                                                   min_views=Settings.youtube_min_views, 
                                                   min_comments=Settings.youtube_min_comments, 
                                                   published_after=datetime.now() - timedelta(days=Settings.youtube_last_n_days))

   



    async def download_youtube_videos_for_keywords(self, keywords: dict[str, str]) -> list[VideoStats]:
        """
        Get youtube videos based on a list of keywords

        Args:
            keywords (dict[str, str]): A dictionary of keywords and their descriptions
            last_n_days (int): The number of days to search for

        Returns:
            results (list): A list of dictionaries with video details
        """
        videos:list[VideoStats] = []
        for k,v in keywords.items():
           self.logger.info(f"Downloading videos for {v}")

           try:
               # check if the file exists
               if self.storage.has_item(f"videos_{k}.json") and not Settings.youtube_overwrite_files:
                   self.logger.info(f"File already exists for {k}")
                   continue
               
               videos = await self.download_youtube_videos(v)
               if videos:
                   self.logger.info(f"Downloaded {len(videos)} videos and saving to {self.storage_dir}/videos_{k}.json")
                   self.youtube_searcher.save_to_json(videos, f"{self.storage_dir}/videos_{k}.json")
               else:
                   self.logger.error(f"No videos found for {k}")
               # pause for 1 second
               await asyncio.sleep(1)
           except Exception as e:
               self.logger.error(f"Error downloading videos for {k}: {type(e).__name__} - {e}")
        return videos


    async def download_youtube_videos_for_ontology(self, ontology: TopicOntology, input: str):
        """
        Get youtube videos based on a ontology
        
        Args:
            ontology (TopicOntology): The ontology to search for
            last_n_days (int): The number of days to search for

        Returns:
            results (list): A list of dictionaries with video details
        """
        keywords = ontology.get_keywords(input)
        return await self.download_youtube_videos_for_keywords(keywords)
    

    def load_videos_from_files(self, input: str) -> list[VideoStats]:
        """
        Load videos from files

        Args:
            input (str): The input to search for. This is the suffix in the ontology file. 
            E.g. For input "machine learning" the ontology file is "ontology_machine learning.json"
            and the videos file is "videos_<leaf topics>.json"
        Returns:
            videos (list): A list of dictionaries with video details
        """
        # load ontology
        ontology = TopicOntology.load_ontology(f"{self.storage_dir}/ontology_{input}.json", self.storage)
        keywords = ontology.get_keywords()


        videos = self.youtube_searcher.load_youtube_videos_from_files(keywords)
        return videos
    
