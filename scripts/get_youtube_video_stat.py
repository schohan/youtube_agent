
from app.common.content.youtube_search import YouTubeSearcher
from app.configs.settings import Settings
from app.common.storage.storage_factory import StorageFactory

def get_youtube_video_stat(video_id: str):
    """
    Get the video stats for the videos in the raw_files_dir

    args:
        - search_term: the search term to get the video stats for

    returns:
        - None
    """
    api_key = Settings.youtube_api_key
    if not api_key:
        raise ValueError("Please set YOUTUBE_API_KEY environment variable")
    
    storage = StorageFactory.get_storage(Settings.storage_type, Settings.raw_files_dir)
    searcher = YouTubeSearcher(api_key, storage)

    # get all the files in the raw_files_dir
    stats = searcher.get_video_stats([video_id], min_views=100, min_comments=0)
    print(stats)
    return stats
   

if __name__ == "__main__":
    get_youtube_video_stat("LwhFrMUU_qQ")