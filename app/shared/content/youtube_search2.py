from typing import List, Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from datetime import datetime
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import logging
from app.configs.settings import Settings
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import json

@dataclass
class VideoStats:
    video_id: str
    title: str
    description: str
    published_at: datetime
    view_count: int
    comment_count: int
    like_count: int
    favorite_count: int
    channel_title: str
    transcript: str
    url: str


class YouTubeSearcher:
    def __init__(self, api_key: str):
        """Initialize YouTube API client."""
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.logger = logging.getLogger(__name__)

    def search_videos(
        self,
        query: str,
        max_results: int = 50,
        min_views: Optional[int] = None,
        min_comments: Optional[int] = None,
        published_after: Optional[datetime] = None,
        relevance_language: Optional[str] = None
    ) -> List[VideoStats]:
        """
        Search YouTube videos with filtering.
        
        Args:
            query: Search term
            max_results: Maximum number of results to return
            min_views: Minimum view count filter
            min_comments: Minimum comment count filter
            published_after: Filter videos published after this date
        
        Returns:
            List of VideoStats objects containing filtered video information
        """
        try:
            # Initial search request
            search_request = self.youtube.search().list(
                q=query,
                part='id,snippet',
                type='video',
                maxResults=min(max_results, 50),  # API limit is 50
                order='relevance',
                publishedAfter=published_after.isoformat() + 'Z' if published_after else None,
                relevanceLanguage=relevance_language
            )
            
            search_response = search_request.execute()
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            if not video_ids:
                self.logger.warning(f"No videos found for query: {query}")
                return []
            
            # Get detailed video statistics
            return self._get_filtered_video_stats(
                video_ids,
                min_views,
                min_comments
            )
            
        except HttpError as e:
            self.logger.error(f"YouTube API error: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            raise


    def _save_to_json(self, videos: list[VideoStats], path: str):
        """Save video details to JSON file."""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                videos_data = [
                    {**video.__dict__,'published_at': video.published_at.isoformat()} for video in videos
                ]
                json.dump(videos_data, f, ensure_ascii=True, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving to JSON: {str(e)}")        




    def _get_video_transcript(self, video_id: str) -> str:
        """Fetch video transcript using youtube_transcript_api."""
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            return ' '.join([line['text'] for line in transcript_list])
        except TranscriptsDisabled:
            self.logger.warning(f"Transcripts are disabled for video {video_id}")
            return ""
        except Exception as e:
            self.logger.warning(f"Error fetching transcript for video {video_id}: {str(e)}")
            return ""            


    def _get_filtered_video_stats(
        self,
        video_ids: List[str],
        min_views: Optional[int],
        min_comments: Optional[int]
    ) -> List[VideoStats]:
        """Get and filter detailed video statistics."""
        
        try:
            # Get video statistics in batches
            videos_data = []
            for i in range(0, len(video_ids), 50):
                batch = video_ids[i:i + 50]
                videos_request = self.youtube.videos().list(
                    part='snippet,statistics',
                    id=','.join(batch)
                )
                videos_data.extend(videos_request.execute().get('items', []))
            
            # Process and filter videos
            filtered_videos = []
            for video in videos_data:
                try:
                    stats = video['statistics']
                    view_count = int(stats.get('viewCount', 0))
                    comment_count = int(stats.get('commentCount', 0))
                    
                    # Apply filters
                    if min_views and view_count < min_views:
                        continue
                    if min_comments and comment_count < min_comments:
                        continue
                    
                    # get transcript
                    transcript = self._get_video_transcript(video['id'])

                    if not transcript:
                        continue

                    filtered_videos.append(VideoStats(
                        video_id=video['id'],
                        title=video['snippet']['title'],
                        description=video['snippet']['description'],
                        published_at=datetime.strptime(
                            video['snippet']['publishedAt'],
                            '%Y-%m-%dT%H:%M:%SZ'
                        ),
                        view_count=view_count,
                        comment_count=comment_count,
                        like_count=int(stats.get('likeCount', 0)),
                        favorite_count=int(stats.get('favoriteCount', 0)),
                        channel_title=video['snippet']['channelTitle'],
                        transcript=transcript,
                        url=f"https://youtube.com/watch?v={video['id']}"
                    ))
                    
                except (KeyError, ValueError) as e:
                    self.logger.warning(f"Error processing video {video.get('id')}: {str(e)}")
                    continue
            
            return sorted(filtered_videos, key=lambda x: x.view_count, reverse=True)
            
        except Exception as e:
            self.logger.error(f"Error getting video statistics: {str(e)}")
            raise


def format_number(num: int) -> str:
    """Format large numbers for display."""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    if num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)


# Example usage
def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize with your API key
    api_key = Settings.youtube_api_key
    if not api_key:
        raise ValueError("Please set YOUTUBE_API_KEY environment variable")
    
    searcher = YouTubeSearcher(api_key)
    
    # Search parameters
    search_term = input("Enter your topic for video extraction: ")  
    min_views = 1000
    min_comments = 10
    
    try:
        videos = searcher.search_videos(
            query=search_term,
            max_results=5,
            min_views=min_views,
            min_comments=min_comments,
            published_after=datetime(2024, 1, 1),
            relevance_language='en'
        )
        
        # save to json
        searcher._save_to_json(videos, f"data/raw/videos_{search_term}.json")

        # Print results
        print(f"\nTop videos for '{search_term}':")
        print("-" * 80)
        
        for i, video in enumerate(videos, 1):
            print(f"\n\n{i}->. {video.title}")
            print(f"Channel: {video.channel_title}")
            print(f"Views: {format_number(video.view_count)} | "
                  f"Comments: {format_number(video.comment_count)} | "
                  f"Likes: {format_number(video.like_count)}")
            print(f"Transcript: {video.transcript}")
            print(f"URL: {video.url}")
            print(f"Published At: {video.published_at}")
            
    except Exception as e:
        logging.error(f"Error searching videos: {str(e)}")

if __name__ == "__main__":
    main()