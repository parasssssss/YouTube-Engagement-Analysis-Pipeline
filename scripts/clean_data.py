# scripts/clean_data.py

import pandas as pd
from textblob import TextBlob

def clean_comments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean comments DataFrame and add sentiment analysis.
    """
    # Drop duplicates & missing text
    df = df.drop_duplicates(subset=['video_id', 'author', 'text'])
    df = df.dropna(subset=['text'])
    
    # Strip whitespace
    df['text'] = df['text'].str.strip()
    
    # Sentiment
    df['polarity'] = df['text'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['sentiment'] = df['polarity'].apply(
        lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'neutral')
    )
    
    # Convert published_at
    df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce')
    
    # Save cleaned CSV
    df.to_csv('dataset/comments_cleaned.csv', index=False, encoding='utf-8')
    print(f"Cleaned comments saved. Total comments: {len(df)}")
    
    return df