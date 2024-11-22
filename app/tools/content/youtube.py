from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from dataclasses import dataclass

@dataclass
class YoutubeSnippet:
    """
    A dataclass to hold YouTube video snippet details
    """
    video_id: str
    title: str
    description: str
    views: int
    thumbnails: dict
    captions: list
    transcript: str



class Youtube:
    """
    A class to interact with the YouTube API
    """

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
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        request = youtube.search().list(
            q=search_term,
            part='snippet',
            type='video',
            maxResults=max_results
        )
        
        response = request.execute()
        video_details = []
        
        for item in response['items']:
            print(item)
            
            snippet = YoutubeSnippet(
                video_id=item['id']['videoId'],
                title=item['snippet']['title'],
                description=item['snippet']['description'],
                views=0,
                thumbnails=item['snippet']['thumbnails'],
                captions=[],
                transcript=""
            )
            # video_id = item['id']['videoId']
            # video_title = item['snippet']['title']
            # video_thumbnails = item['snippet']['thumbnails']
            # video_description = item['snippet']['description']

            # Get video statistics
            video_request = youtube.videos().list(
                part='statistics',
                id=snippet.video_id
            )
            video_response = video_request.execute()            
            #view_count = video_response['items'][0]['statistics']['viewCount']
            snippet.views = video_response['items'][0]['statistics']['viewCount']
                        
            # Get captions
            captions = []
            captions_request = youtube.captions().list(
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

            # Get transcript
            try:
                transcriptObj = YouTubeTranscriptApi.get_transcript(snippet.video_id)
                transcript = ' '.join([line['text'] for line in transcriptObj])
            except Exception as e:
                print(e)
                transcript = ""

            snippet.transcript = transcript

            # Append video details to list
            # video_details.append({
            #     'id': video_id,
            #     'title': video_title,
            #     'description': video_description,
            #     'views': view_count,
            #     'thumbnails': video_thumbnails,
            #     'captions': captions,
            #     'transcript': transcript
            # })
            video_details.append(snippet)
        
        return video_details

