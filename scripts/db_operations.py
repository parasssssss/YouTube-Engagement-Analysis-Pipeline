

import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        dbname="youtube_db",
        user="postgres",
        password=os.getenv("DATABASE_PASSWORD"),
        port=5432
    )
    return conn, conn.cursor()

def create_table(cursor, conn):
    query = """
    CREATE TABLE IF NOT EXISTS youtube_comments (
        video_id TEXT,
        video_title TEXT,
        views BIGINT,
        video_likes BIGINT,
        video_total_comments BIGINT,
        author TEXT,
        published_at TIMESTAMP,
        text TEXT,
        like_count INT,
        polarity FLOAT,
        sentiment TEXT,
        PRIMARY KEY (video_id, author, published_at)
    );
    """
    cursor.execute(query)
    conn.commit()

def upsert_comments(df, cursor, conn):

    records = list(df[[
        'video_id','video_title','views','video_likes','video_total_comments',
        'author','published_at','text','like_count','polarity','sentiment'
    ]].itertuples(index=False, name=None))

    query = """
    INSERT INTO youtube_comments (
        video_id,
        video_title,
        views,
        video_likes,
        video_total_comments,
        author,
        published_at,
        text,
        like_count,
        polarity,
        sentiment
    )
    VALUES %s
    ON CONFLICT (video_id, author, published_at)
    DO UPDATE SET
        text = EXCLUDED.text,
        like_count = EXCLUDED.like_count,
        polarity = EXCLUDED.polarity,
        sentiment = EXCLUDED.sentiment;
    """

    execute_values(cursor, query, records)
    conn.commit()

    print(f"{len(records)} rows upserted")