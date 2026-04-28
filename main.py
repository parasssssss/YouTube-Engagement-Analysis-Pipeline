# main.py

from scripts.fetch_comments import fetch_comments
from scripts.clean_data import clean_comments
from scripts.analyze_data import analyze_engagement
from scripts.db_operations import connect_db, create_table, upsert_comments


def main():
    
    keyword = input("Enter keyword (default: iPhone): ") or "iPhone"

    
    raw_df = fetch_comments(keyword=keyword, max_videos=5, max_comments=100)
    
  
    cleaned_df = clean_comments(raw_df)
    
    
    analyzed_df = analyze_engagement(cleaned_df)
    
    
    conn, cursor = connect_db()
    
    create_table(cursor, conn)
    upsert_comments(analyzed_df, cursor, conn)
    
    cursor.close()
    conn.close()

    print("Pipeline completed successfully!")


if __name__ == "__main__":
    main()
