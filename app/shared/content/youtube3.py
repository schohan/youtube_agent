from dataclasses import dataclass
from datetime import date
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import logging
import os
from concurrent.futures import ThreadPoolExecutor
import json
from datetime import datetime
from app.configs.settings import Settings
import time

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
    view_count: int = 0
    like_count: int = 0 
    favorite_count: int = 0   
    comment_count: int = 0

class YouTubeDownloader:
    def __init__(self, api_key: str):
        """Initialize YouTube API client."""
        self.youtube = build('youtube', 'v3', developerKey=api_key, cache_discovery=False)
        self.logger = logging.getLogger(__name__)

    def _get_video_captions(self, video_id: str) -> List[dict]:
        """Fetch available captions for a video."""
        try:
            captions_response = self.youtube.captions().list(
                part='snippet',
                videoId=video_id
            ).execute()
            
            return [
                {
                    'language': caption['snippet']['language'],
                    'trackKind': caption['snippet']['trackKind'],
                    'isDraft': caption['snippet'].get('isDraft', False),
                    'isAutoSynced': caption['snippet'].get('isAutoSynced', False)
                }
                for caption in captions_response.get('items', [])
            ]
        except HttpError as e:
            self.logger.warning(f"Error fetching captions for video {video_id}: {str(e)}")
            return []


    def _get_video_transcript(self, video_id: str) -> str:
        """Fetch video transcript using youtube_transcript_api."""
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            return ' '.join(item['text'] for item in transcript_list)
        except TranscriptsDisabled:
            self.logger.warning(f"Transcripts are disabled for video {video_id}")
            return ""
        except Exception as e:
            self.logger.warning(f"Error fetching transcript for video {video_id}: {str(e)}")
            return ""


    def get_video_details(self, video_id: str) -> Optional[YoutubeSnippet]:
        """Get complete details for a single video."""
        try:
            # Add retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    video_response = self.youtube.videos().list(
                        part='snippet,statistics',
                        id=video_id
                    ).execute()

                    if not video_response.get('items'):
                        return None

                    video = video_response['items'][0]
                    snippet = video['snippet']
                    statistics = video.get('statistics', {})

                    # Get captions and transcript
                    captions = self._get_video_captions(video_id)
                    print(f"Captions: {captions}")                    
                    print(f"Statistics: {statistics}")

                    transcript = self._get_video_transcript(video_id)
                    print(f"Transcript: {transcript}")
                    
                    return YoutubeSnippet(
                        videoId=video_id,
                        publishedAt=date.fromisoformat(snippet['publishedAt'][:10]),
                        title=snippet['title'],
                        description=snippet['description'],
                        thumbnails=snippet['thumbnails'],
                        captions=captions,
                        transcript=transcript,
                        view_count=int(statistics.get('viewCount', 0)),
                        like_count=int(statistics.get('likeCount', 0)),
                        favorite_count=int(statistics.get('favoriteCount', 0)),
                        comment_count=int(statistics.get('commentCount', 0))
                    )

                except HttpError as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(1)  # Wait before retry

        except Exception as e:
            self.logger.error(f"Error getting details for video {video_id}: {str(e)}")
            return None

    def search_videos(
        self,
        query: str,
        max_results: int = 50,
        min_views: Optional[int] = None,
        min_comments: Optional[int] = None,
        published_after: Optional[datetime] = None,
        download_path: Optional[str] = None
    ) -> List[YoutubeSnippet]:
        """
        Search YouTube videos and get complete details including thumbnails, captions, and transcripts.
        
        Args:
            query: Search term
            max_results: Maximum number of results to return
            min_views: Minimum view count filter
            min_comments: Minimum comment count filter
            download_path: Optional path to save video details as JSON
        
        Returns:
            List of YoutubeSnippet objects
        """
        try:
            # Initial search request
            search_response = self.youtube.search().list(
                q=query,
                part='id',
                type='video',
                maxResults=min(max_results, 50),
                order='relevance',
                publishedAfter=published_after.isoformat() + 'Z' if published_after else None
            ).execute()

            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            if not video_ids:
                self.logger.warning(f"No videos found for query: {query}")
                return []

            # Get detailed information for each video using parallel processing
            with ThreadPoolExecutor(max_workers=5) as executor:
                videos = list(filter(None, executor.map(self.get_video_details, video_ids)))

            # Apply filters
            filtered_videos = [
                video for video in videos
                if (min_views is None or video.view_count >= min_views) and
                   (min_comments is None or video.comment_count >= min_comments)
            ]

            # Sort by view count
            filtered_videos.sort(key=lambda x: x.view_count, reverse=True)

            # Save to file if path provided
            if download_path:
                self._save_to_json(filtered_videos, download_path)

            return filtered_videos

        except Exception as e:
            self.logger.error(f"Error in search_videos: {str(e)}")
            raise

    def _save_to_json(self, videos: List[YoutubeSnippet], path: str):
        """Save video details to JSON file."""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                # Convert date objects to string for JSON serialization
                videos_data = [
                    {**video.__dict__,
                     'publishedAt': video.publishedAt.isoformat()}
                    for video in videos
                ]
                json.dump(videos_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving to JSON: {str(e)}")


def format_number(num: int) -> str:
    """Format large numbers for display."""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    if num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)


def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize with your API key
    api_key = Settings.youtube_api_key
    if not api_key:
        raise ValueError("Please set YOUTUBE_API_KEY environment variable")
    
    downloader = YouTubeDownloader(api_key)
    
    # Search parameters
    search_term = input("Enter your topic for video extraction: ")  
    min_views = 1000
    
    try:
        videos = downloader.search_videos(
            query=search_term,
            max_results=20,
            min_views=min_views,
            published_after=datetime(2024, 1, 1),
            download_path="youtube_results.json"
        )
        
        # Print results
        print(f"\nTop videos for '{search_term}':")
        print("-" * 80)
        
        for i, video in enumerate(videos, 1):
            print(f"\n{i}. {video.title}")
            print(f"Views: {format_number(video.view_count)} | "
                f"Comments: {format_number(video.comment_count)} | "
                f"Likes: {format_number(video.like_count)}")
            print(f"Available Captions: {len(video.captions)}")
            print(f"Transcript Length: {len(video.transcript)} chars")
            print(f"Thumbnail URLs:")
            for quality, thumb in video.thumbnails.items():
                print(f"  - {quality}: {thumb['url']}")
            
    except Exception as e:
        logging.error(f"Error searching videos: {str(e)}")

if __name__ == "__main__":
    main()