# scripts/fetch_comments.py

import pandas as pd
from googleapiclient.discovery import build
import time
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_video_stats(youtube, video_ids):
    request = youtube.videos().list(
        part="statistics,snippet",
        id=",".join(video_ids)
    )
    response = request.execute()

    video_data = {}

    for item in response['items']:
        vid = item['id']
        stats = item['statistics']
        snippet = item['snippet']

        video_data[vid] = {
            'video_title': snippet['title'],
            'views': int(stats.get('viewCount', 0)),
            'video_likes': int(stats.get('likeCount', 0)),
            'video_total_comments': int(stats.get('commentCount', 0))
        }

    return video_data


def fetch_comments(keyword: str, max_videos: int = 5, max_comments: int = 100) -> pd.DataFrame:

    API_KEY = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # 🔍 Search videos
    search_request = youtube.search().list(
        q=keyword,
        part='id',
        type='video',
        maxResults=max_videos
    )
    search_response = search_request.execute()

    video_ids = [item['id']['videoId'] for item in search_response['items']]
    print(f"Found {len(video_ids)} videos for keyword '{keyword}'")

    # 🔥 NEW: Fetch video stats
    video_stats = fetch_video_stats(youtube, video_ids)

    # 💬 Fetch comments
    all_comments = []

    for video_id in video_ids:
        print(f"Fetching comments for video: {video_id}")

        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText"
        )

        count = 0

        while request and count < max_comments:
            response = request.execute()

            for item in response['items']:
                snippet = item['snippet']['topLevelComment']['snippet']

                all_comments.append({
                    'video_id': video_id,
                    'video_title': video_stats[video_id]['video_title'],
                    'views': video_stats[video_id]['views'],
                    'video_likes': video_stats[video_id]['video_likes'],
                    'video_total_comments': video_stats[video_id]['video_total_comments'],
                    'author': snippet['authorDisplayName'],
                    'text': snippet['textDisplay'],
                    'published_at': snippet['publishedAt'],
                    'like_count': snippet['likeCount']
                })

                count += 1

            request = youtube.commentThreads().list_next(request, response)
            time.sleep(1)

    df = pd.DataFrame(all_comments)

    os.makedirs('dataset', exist_ok=True)
    df.to_csv('dataset/comments_raw.csv', index=False, encoding='utf-8')

    print(f"Saved {len(df)} comments")

    return df