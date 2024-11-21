from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

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
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            video_thumbnail = item['snippet']['thumbnails']['default']['url']
            
            # Get video statistics
            video_request = youtube.videos().list(
                part='statistics',
                id=video_id
            )
            video_response = video_request.execute()
            
            view_count = video_response['items'][0]['statistics']['viewCount']
            
            # Get captions
            captions_request = youtube.captions().list(
                part='snippet',
                videoId=video_id
            )
            captions_response = captions_request.execute()
            
            captions = []
            for caption in captions_response['items']:
                caption_id = caption['id']
                caption_language = caption['snippet']['language']
                caption_name = caption['snippet']['name']
                captions.append({
                    'id': caption_id,
                    'language': caption_language,
                    'name': caption_name
                })
            
            # Get transcript
            try:
                transcriptObj = YouTubeTranscriptApi.get_transcript(video_id)
                transcript = ' '.join([line['text'] for line in transcriptObj])
            except Exception as e:
                print(e)
                transcript = ""
            
            # Append video details to list
            video_details.append({
                'title': video_title,
                'views': view_count,
                'thumbnail': video_thumbnail,
                'captions': captions,
                'transcript': transcript
            })
        
        return video_details

