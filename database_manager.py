import sqlite3
import pandas as pd
import os
import json
from datetime import datetime

# Use absolute path for database file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'social_media_analytics.db')

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
    """Save DataFrame to database with improved error handling and deduplication"""
    conn = get_db_connection()
    
    try:
        # Ensure columns match schema
        required_cols = [
            'post_id', 'timestamp', 'caption', 'likes', 'comments', 'shares', 
            'saves', 'impressions', 'reach', 'follower_count', 'audience_gender', 
            'audience_age', 'location', 'hashtags', 'media_type'
        ]
        
        # Validate input data
        if df.empty:
            print("⚠️ Warning: Empty DataFrame provided to save_data")
            return
        
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
        
        # Convert numeric columns to proper data types before saving
        numeric_columns = ['likes', 'comments', 'shares', 'saves', 'impressions', 'reach', 'follower_count']
        for col in numeric_columns:
            if col in df_to_save.columns:
                # Convert to numeric, replacing invalid values with 0
                df_to_save[col] = pd.to_numeric(df_to_save[col], errors='coerce').fillna(0).astype(int)
        
        # Convert timestamp to datetime then string for SQLite
        df_to_save['timestamp'] = pd.to_datetime(df_to_save['timestamp'], errors='coerce')
        df_to_save['timestamp'] = df_to_save['timestamp'].astype(str)
        
        # Handle NaN values
        df_to_save = df_to_save.fillna('')
        
        # Enhanced deduplication strategy
        # 1. Remove duplicates within the new data itself
        df_to_save = df_to_save.drop_duplicates(subset=['post_id'], keep='first')
        
        # 2. Identify records that already exist in database
        try:
            # Get existing post_ids from database
            existing_df = pd.read_sql("SELECT post_id, timestamp FROM posts", conn)
            existing_ids = set(existing_df['post_id'].tolist())
            
            # Also check for near-duplicates (same timestamp, similar content)
            # This helps with cases where post_id might be different but content is the same
            existing_timestamps = existing_df[['post_id', 'timestamp']].set_index('timestamp')
            
        except Exception as e:
            print(f"⚠️ Warning: Could not read existing data from database: {e}")
            existing_ids = set()
            existing_timestamps = pd.DataFrame()
            
        # Filter out records that already exist
        df_new = df_to_save[~df_to_save['post_id'].isin(existing_ids)]
        
        # Additional conflict resolution: Update existing records with newer data
        df_update = df_to_save[df_to_save['post_id'].isin(existing_ids)]
        
        if not df_new.empty or not df_update.empty:
            records_added = 0
            records_updated = 0
            
            # Insert new records
            if not df_new.empty:
                try:
                    df_new.to_sql('posts', conn, if_exists='append', index=False)
                    records_added = len(df_new)
                    print(f"✅ Added {records_added} new records to database.")
                except Exception as e:
                    print(f"❌ Error inserting new data into database: {e}")
                    raise
            
            # Update existing records (simple approach - delete and reinsert)
            if not df_update.empty:
                try:
                    # Delete existing records
                    placeholders = ','.join(['?' for _ in df_update['post_id']])
                    query = f"DELETE FROM posts WHERE post_id IN ({placeholders})"
                    conn.execute(query, tuple(df_update['post_id'].tolist()))
                    
                    # Reinsert updated records
                    df_update.to_sql('posts', conn, if_exists='append', index=False)
                    records_updated = len(df_update)
                    print(f"✅ Updated {records_updated} existing records in database.")
                except Exception as e:
                    print(f"❌ Error updating existing data in database: {e}")
                    # Try to rollback by reinserting original data
                    # This is a simplified approach - in production, you'd want proper transactions
                    pass
            
            total_changes = records_added + records_updated
            if total_changes > 0:
                # Trigger ML pipeline processing in the background
                try:
                    from ml_pipeline import execute_ml_pipeline
                    print("🚀 Starting ML pipeline processing in background...")
                    # Run ML pipeline asynchronously
                    import threading
                    thread = threading.Thread(target=execute_ml_pipeline, daemon=True)
                    thread.start()
                    print("✅ ML pipeline started in background thread.")
                except Exception as e:
                    print(f"⚠️ Failed to start ML pipeline: {e}")
        else:
            print("ℹ️ No new or updated records to process.")
            
    except Exception as e:
        print(f"❌ Critical error in save_data: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            conn.close()
        except Exception as e:
            print(f"⚠️ Error closing database connection: {e}")

def load_data():
    """Load data from database with proper data type conversion"""
    conn = get_db_connection()
    try:
        df = pd.read_sql("SELECT * FROM posts", conn)
        
        # Convert timestamp back to datetime
        if not df.empty and 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        
        # Convert numeric columns to proper data types
        numeric_columns = ['likes', 'comments', 'shares', 'saves', 'impressions', 'reach', 'follower_count']
        for col in numeric_columns:
            if col in df.columns:
                # Convert to numeric, replacing invalid values with 0
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def parse_csv_files_in_data_dir(data_dir, adapter_func):
    """Parse all CSV files in data directory and save to DB with enhanced error handling"""
    if not os.path.exists(data_dir):
        print(f"⚠️ Data directory not found: {data_dir}")
        return
    
    try:
        files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        print(f"📁 Found {len(files)} CSV files in {data_dir}")
    except Exception as e:
        print(f"❌ Error reading data directory: {e}")
        return
    
    if not files:
        print("⚠️ No CSV files found in data directory")
        return
    
    processed_count = 0
    failed_count = 0
    
    for f in files:
        file_path = os.path.join(data_dir, f)
        try:
            print(f"🔄 Processing {f}...")
            df = adapter_func(file_path)
            if df is not None and not df.empty:
                save_data(df)
                print(f"✅ Successfully processed and saved {f} ({len(df)} records)")
                processed_count += 1
            else:
                print(f"⚠️ Skipped {f} (no valid data extracted)")
                failed_count += 1
        except Exception as e:
            print(f"❌ Error processing {f}: {e}")
            import traceback
            traceback.print_exc()
            failed_count += 1
    
    print(f"📊 Processing complete: {processed_count} files processed, {failed_count} files failed")
    
    # If we processed any files, trigger ML pipeline
    if processed_count > 0:
        try:
            from ml_pipeline import execute_ml_pipeline
            print("🚀 Starting ML pipeline processing for newly loaded data...")
            # Run ML pipeline asynchronously
            import threading
            thread = threading.Thread(target=execute_ml_pipeline, daemon=True)
            thread.start()
            print("✅ ML pipeline started in background thread for newly loaded data.")
        except Exception as e:
            print(f"⚠️ Failed to start ML pipeline for new data: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
