# scripts/analyze_data.py

import pandas as pd

def analyze_engagement(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute engagement metrics, sentiment summary, comments per video.
    Returns the same DataFrame (for DB insertion).
    """
    # Metrics
    total_comments = len(df)
    total_likes = df['like_count'].sum()
    avg_likes = df['like_count'].mean()
    
    # Sentiment
    sentiment_counts = df['sentiment'].value_counts()
    
    # Comments per video
    comments_per_video = df.groupby('video_id')['text'].count()
    
    # Save summary
    summary_df = pd.DataFrame({
        'metric': ['total_comments', 'total_likes', 'average_likes'],
        'value': [total_comments, total_likes, avg_likes]
    })
    summary_df.to_csv('reports/engagement_summary.csv', index=False)
    
    print("\nEngagement Metrics:")
    print(summary_df)
    print("\nSentiment Counts:")
    print(sentiment_counts)
    print("\nTop 5 Videos by Comments:")
    print(comments_per_video.sort_values(ascending=False).head(5))
    
    return df