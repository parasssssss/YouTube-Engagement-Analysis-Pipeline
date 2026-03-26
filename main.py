# main.py

from scripts.fetch_comments import fetch_comments
from scripts.clean_data import clean_comments
from scripts.analyze_data import analyze_engagement
from scripts.db_operations import connect_db, create_table, upsert_comments
import os


def main():
    # 1️⃣ Fetch comments
    raw_df = fetch_comments(keyword='Galaxy S26', max_videos=5, max_comments=100)
    
    # 2️⃣ Clean comments
    cleaned_df = clean_comments(raw_df)
    
    # 3️⃣ Analyze engagement
    analyzed_df = analyze_engagement(cleaned_df)
    
    # 4️⃣ PostgreSQL
    conn, cursor = connect_db(
        host='localhost',
        dbname='youtube_db',
        user='postgres',
        password=os.getenv("DATABASE_PASSWORD")
    )
    
    create_table(cursor, conn)
    upsert_comments(analyzed_df, cursor, conn)
    
    cursor.close()
    conn.close()
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()