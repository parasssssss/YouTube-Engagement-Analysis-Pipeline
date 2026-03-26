# scripts/fetch_comments.py

import pandas as pd
from googleapiclient.discovery import build
import time
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_comments(keyword: str, max_videos: int = 5, max_comments: int = 100) -> pd.DataFrame:
    """
    Fetch YouTube comments for videos matching the keyword.
    Returns a DataFrame.
    """
    API_KEY = os.getenv('YOUTUBE_API_KEY')
    
   
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    # Search videos
    search_request = youtube.search().list(
        q=keyword,
        part='id',
        type='video',
        maxResults=max_videos
    )
    search_response = search_request.execute()
    video_ids = [item['id']['videoId'] for item in search_response['items']]
    print(f"Found {len(video_ids)} videos for keyword '{keyword}'")
    
    # Fetch comments
    all_comments = []
    for video_id in video_ids:
        print(f"Fetching comments for video: {video_id}")
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText"
        )
        while request and len(all_comments) < max_comments * len(video_ids):
            response = request.execute()
            for item in response['items']:
                snippet = item['snippet']['topLevelComment']['snippet']
                all_comments.append({
                    'video_id': video_id,
                    'author': snippet['authorDisplayName'],
                    'text': snippet['textDisplay'],
                    'published_at': snippet['publishedAt'],
                    'like_count': snippet['likeCount']
                })
            request = youtube.commentThreads().list_next(request, response)
            time.sleep(1)  # avoid rate limits
    
    df = pd.DataFrame(all_comments)
    
    # Save raw comments
    os.makedirs('dataset', exist_ok=True)
    df.to_csv('dataset/comments_raw.csv', index=False, encoding='utf-8')
    print(f"Saved {len(df)} comments to dataset/comments_raw.csv")
    
    return df