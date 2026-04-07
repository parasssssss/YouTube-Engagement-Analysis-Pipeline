

import pandas as pd

def analyze_engagement(df: pd.DataFrame) -> pd.DataFrame:

   
    total_comments = len(df)
    total_likes = df['like_count'].sum()
    avg_likes = df['like_count'].mean()

   
    sentiment_counts = df['sentiment'].value_counts()

    
    video_perf = df.groupby(['video_id', 'video_title']).agg({
        'views': 'first',
        'video_likes': 'first',
        'video_total_comments': 'first',
        'text': 'count'
    }).rename(columns={'text': 'fetched_comments'})

   
    video_perf['engagement_rate'] = (
        (video_perf['video_likes'] + video_perf['video_total_comments']) 
        / video_perf['views']
    )

  
    top_videos = video_perf.sort_values(by='engagement_rate', ascending=False).head(5)

  
    summary_df = pd.DataFrame({
        'metric': ['total_comments', 'total_likes', 'average_likes'],
        'value': [total_comments, total_likes, avg_likes]
    })

    summary_df.to_csv('reports/engagement_summary.csv', index=False)
    video_perf.to_csv('reports/video_performance.csv')

    print("\n Engagement Metrics:")
    print(summary_df)

    print("\n Sentiment Counts:")
    print(sentiment_counts)

    print("\n Top Videos by Engagement Rate:")
    print(top_videos)

    return df