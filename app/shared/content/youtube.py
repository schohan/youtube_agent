# DEPRECATED. This class is deprecated. Use youtube_search.py instead.
from datetime import date
from logging import getLogger
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from dataclasses import dataclass
from datetime import date



@dataclass
class YoutubeSnippet:
    """
    A dataclass to hold YouTube video snippet details
    """
    videoId: str
    publishedAt: date
    title: str
    description: str
    thumbnails: dict
    captions: list
    transcript: str
    viewCount: int = 0
    likeCount: int = 0 
    favoriteCount: int = 0   
    commentCount: int = 0
    


class Youtube:
    """
    A class to interact with the YouTube API
    """
    logger = getLogger(__name__)

    @staticmethod
    def search_youtube_videos(search_term, api_key, max_results=10):
        """
        Search for videos on YouTube based on a search term
        Args:
            search_term (str): The search term to use
            api_key (str): The YouTube API key
            max_results (int): The maximum number of results to return

        Returns:
            video_details (list): A list of dictionaries with video details        
        """
        youtubeClient = build('youtube', 'v3', developerKey=api_key)
        
        request = youtubeClient.search().list(
            q=search_term,
            part='snippet',
            type='video',
            maxResults=max_results
        )
        
        response = request.execute()
        video_details = []
        
        for item in response['items']:
            Youtube.logger.info(item)

            thumbnails = item['snippet'].get('thumbnails', {})
            snippet = YoutubeSnippet(
                videoId=item['id']['videoId'],
                publishedAt=item['snippet']['publishedAt'],
                title=item['snippet']['title'],
                description=item['snippet']['description'],
                thumbnails=thumbnails,
                captions=[],
                transcript=""
            ) 

            # Get video statistics
            Youtube.add_stats(youtubeClient, snippet)

            # Get captions            
            Youtube.add_captions(youtubeClient, snippet)
            
            # Get transcript
            Youtube.add_transcript(snippet)

            # Append video details to list
            video_details.append(snippet)

        return video_details


    @staticmethod
    def add_transcript(snippet):
        try:
            transcriptObj = YouTubeTranscriptApi.get_transcript(snippet.video_id)
            transcript = ' '.join([line['text'] for line in transcriptObj])
        except Exception as e:
            print(e)
            transcript = ""

        snippet.transcript = transcript




    @staticmethod
    def add_captions(youtubeClient, snippet):
        captions = []
        captions_request = youtubeClient.captions().list(
                part='snippet',
                videoId=snippet.video_id
            )
        captions_response = captions_request.execute()
        for caption in captions_response['items']:
            caption_id = caption['id']
            caption_language = caption['snippet']['language']
            caption_name = caption['snippet']['name']
            captions.append({
                    'id': caption_id,
                    'language': caption_language,
                    'name': caption_name
                })
        snippet.captions = captions
        return youtubeClient
    
   
    @staticmethod
    def add_stats(youtubeClient, snippet):
        video_request = youtubeClient.videos().list(
                part='statistics',
                id=snippet.video_id
            )
        video_response = video_request.execute()            
        snippet.viewCount = video_response['items'][0]['statistics']['viewCount']
        snippet.likeCount = video_response['items'][0]['statistics']['likeCount']
        snippet.favoriteCount = video_response['items'][0]['statistics']['favoriteCount']
        snippet.commentCount = video_response['items'][0]['statistics']['commentCount']
        return youtubeClient
