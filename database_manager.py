import sqlite3
import pandas as pd
import os
import json
from datetime import datetime

DB_FILE = 'social_media_analytics.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with schema"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Create table for social media posts
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            post_id TEXT PRIMARY KEY,
            timestamp DATETIME,
            caption TEXT,
            likes INTEGER,
            comments INTEGER,
            shares INTEGER,
            saves INTEGER,
            impressions INTEGER,
            reach INTEGER,
            follower_count INTEGER,
            audience_gender TEXT,
            audience_age TEXT,
            location TEXT,
            hashtags TEXT,
            media_type TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_data(df):
    """Save DataFrame to database"""
    conn = get_db_connection()
    
    # Ensure columns match schema
    required_cols = [
        'post_id', 'timestamp', 'caption', 'likes', 'comments', 'shares', 
        'saves', 'impressions', 'reach', 'follower_count', 'audience_gender', 
        'audience_age', 'location', 'hashtags', 'media_type'
    ]
    
    # Add missing columns with default values
    for col in required_cols:
        if col not in df.columns:
            if col == 'timestamp':
                df[col] = datetime.now()
            elif col in ['likes', 'comments', 'shares', 'saves', 'impressions', 'reach', 'follower_count']:
                df[col] = 0
            else:
                df[col] = ''
                
    # Select only required columns
    df_to_save = df[required_cols].copy()
    
    # Convert timestamp to string for SQLite
    df_to_save['timestamp'] = df_to_save['timestamp'].astype(str)
    
    try:
        # Use 'replace' or 'append'. 'append' is safer to not lose old data, 
        # but since we have a PK, we might face conflicts.
        # Ideally we perform an upsert. Pandas to_sql doesn't support upsert natively easily for SQLite.
        # For simplicity in this context, we will append and ignore errors (or simple replace if user wants to overwrite).
        # Given the user request "user are upload thre data", let's assume appending is better but we need to handle duplicates.
        
        # We'll use a loop for safer upsert-like behavior or just use to_sql with 'append' and handle PrimaryKeyError by reading first.
        
        # Simple approach: Read existing IDs, filter new DF, append new rows.
        existing_ids = pd.read_sql("SELECT post_id FROM posts", conn)['post_id'].tolist()
        df_new = df_to_save[~df_to_save['post_id'].isin(existing_ids)]
        
        if not df_new.empty:
            df_new.to_sql('posts', conn, if_exists='append', index=False)
            print(f"Added {len(df_new)} new records.")
        else:
            print("No new records to add.")
            
    except Exception as e:
        print(f"Error saving data: {e}")
    finally:
        conn.close()

def load_data():
    """Load data from database"""
    conn = get_db_connection()
    try:
        df = pd.read_sql("SELECT * FROM posts", conn)
        
        # Convert timestamp back to datetime
        if not df.empty and 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def parse_csv_files_in_data_dir(data_dir, adapter_func):
    """Parse all CSV files in data directory and save to DB"""
    if not os.path.exists(data_dir):
        return
    
    files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    for f in files:
        file_path = os.path.join(data_dir, f)
        try:
            print(f"Processing {f}...")
            df = adapter_func(file_path)
            save_data(df)
            print(f"Successfully processed and saved {f}")
        except Exception as e:
            print(f"Error processing {f}: {e}")

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
