"""
Data Adapter for Social Media Analytics Dashboard
Handles multiple CSV formats and converts them to standard format
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re


def detect_csv_format(df):
    """Detect the format of uploaded CSV"""
    columns = [str(col).lower().strip() for col in df.columns]
    
    # Check for Instagram post-level export (new format)
    if 'post id' in columns or 'account username' in columns or 'permalink' in columns:
        return 'instagram_post_export'
    
    # Check for Facebook/Instagram video analytics export
    if any('3-second video views' in str(col).lower() for col in df.columns):
        return 'facebook_video_export'
    
    # Check for standard format
    if 'post_id' in columns and 'timestamp' in columns:
        return 'standard'
    
    return 'unknown'


def clean_instagram_post_export(df):
    """Convert Instagram post-level export to standard format with enhanced validation"""
    
    # Validate input
    if df.empty:
        raise ValueError("Empty DataFrame provided to clean_instagram_post_export")
    
    standard_data = []
    error_count = 0
    
    for idx, row in df.iterrows():
        try:
            # Extract post ID
            post_id = str(row.get('Post ID', f'post_{idx:04d}')).strip()
            if not post_id or post_id.lower() == 'nan':
                post_id = f'post_{idx:04d}'
            
            # Parse timestamp
            timestamp_str = str(row.get('Publish time', '')).strip()
            if not timestamp_str or timestamp_str.lower() == 'nan':
                # Try to get timestamp from other columns
                timestamp_str = str(row.get('Date', '')).strip()
                
            timestamp = None
            if timestamp_str and timestamp_str.lower() != 'nan':
                try:
                    timestamp = pd.to_datetime(timestamp_str, format='%m/%d/%Y %H:%M', errors='coerce')
                    if pd.isna(timestamp):
                        timestamp = pd.to_datetime(timestamp_str, errors='coerce')
                except:
                    timestamp = pd.Timestamp.now()
            else:
                timestamp = pd.Timestamp.now()
            
            if pd.isna(timestamp):
                timestamp = pd.Timestamp.now()
            
            # Extract metrics with enhanced validation
            views = safe_int(row.get('Views', 0))
            reach = safe_int(row.get('Reach', 0))
            likes = safe_int(row.get('Likes', 0))
            comments = safe_int(row.get('Comments', 0))
            shares = safe_int(row.get('Shares', 0))
            follows = safe_int(row.get('Follows', 0))
            saves = safe_int(row.get('Saves', 0))
            
            # Validate metrics (must be non-negative)
            views = max(0, views)
            reach = max(0, reach)
            likes = max(0, likes)
            comments = max(0, comments)
            shares = max(0, shares)
            follows = max(0, follows)
            saves = max(0, saves)
            
            # Use Views as impressions if available
            impressions = views if views > 0 else reach
            if impressions == 0:
                impressions = max(likes * 10, 100)
            
            # Ensure reach is reasonable
            if reach == 0:
                reach = int(impressions * 0.75)
            
            # Extract description/caption
            caption = str(row.get('Description', '')).strip()
            if caption.lower() == 'nan':
                caption = ''
            caption = caption[:200]  # Limit length
            
            # Determine media type
            post_type = str(row.get('Post type', 'IG image')).lower().strip()
            if post_type == 'nan':
                post_type = 'ig image'
                
            if 'reel' in post_type or 'video' in post_type:
                media_type = 'Video'
            elif 'carousel' in post_type:
                media_type = 'Carousel'
            else:
                media_type = 'Image'
            
            # Extract hashtags from description
            hashtags = extract_hashtags(caption)
            
            # Estimate follower count based on follows and date
            base_followers = 10000
            if not pd.isna(timestamp):
                start_date = pd.Timestamp('2019-01-01')
                days_diff = int((timestamp - start_date).days)
                follower_count = base_followers + (days_diff * 3) + (follows * 100)
            else:
                follower_count = base_followers + (follows * 100)
            
            # Ensure follower count is reasonable
            follower_count = max(0, follower_count)
            
            # Demographics - default values
            gender = 'Mixed'
            age = '18-24'
            location = 'India'
            
            # Create standard record
            record = {
                'post_id': post_id,
                'timestamp': timestamp,
                'caption': caption if caption else f'Post from {timestamp.strftime("%B %d, %Y")}',
                'likes': likes,
                'comments': comments,
                'shares': shares,
                'saves': saves,
                'impressions': impressions,
                'reach': reach,
                'follower_count': follower_count,
                'audience_gender': gender,
                'audience_age': age,
                'location': location,
                'hashtags': hashtags,
                'media_type': media_type
            }
            
            standard_data.append(record)
        
        except Exception as e:
            error_count += 1
            if error_count <= 5:  # Only log first 5 errors to avoid spam
                print(f"⚠️ Warning: Error processing row {idx}: {e}")
            continue
    
    if error_count > 0:
        print(f"⚠️ Encountered {error_count} errors while processing data. Successfully processed {len(standard_data)} records.")
    
    if len(standard_data) == 0:
        raise ValueError("No valid data could be extracted from the file")
    
    print(f"✅ Successfully converted {len(standard_data)} Instagram posts to standard format")
    return pd.DataFrame(standard_data)


def clean_facebook_video_export(df):
    """Convert Facebook video analytics export to standard format with enhanced validation"""
    
    # Validate input
    if df.empty:
        raise ValueError("Empty DataFrame provided to clean_facebook_video_export")
    
    # Skip header rows if present
    if df.iloc[0].astype(str).str.contains('Title|Row Labels', case=False).any():
        # Find the actual data start
        for i in range(min(5, len(df))):
            if pd.notna(df.iloc[i, 0]) and '/' in str(df.iloc[i, 0]):
                df = df.iloc[i:].reset_index(drop=True)
                break
    
    # Remove Grand Total row
    df = df[~df.iloc[:, 0].astype(str).str.contains('Grand Total', case=False, na=False)]
    
    # Remove rows with all NaN
    df = df.dropna(how='all')
    
    if df.empty:
        raise ValueError("No valid data after cleaning headers and totals")
    
    # Get the date column (first column)
    date_col = df.columns[0]
    
    standard_data = []
    error_count = 0
    
    for idx, row in df.iterrows():
        try:
            # Extract date/timestamp
            date_str = str(row[date_col]).strip()
            if date_str == 'nan' or date_str == '' or date_str.lower() == 'nan':
                continue
            
            # Parse date
            try:
                timestamp = pd.to_datetime(date_str, errors='coerce')
            except:
                continue
            
            if pd.isna(timestamp):
                continue
            
            # Extract metrics with enhanced validation
            views_3sec = safe_int(row.get('Sum of 3-second video views', 0))
            views_1min = safe_int(row.get('Sum of 1-minute video views', 0))
            reactions = safe_int(row.get('Sum of Reactions', 0))
            comments = safe_int(row.get('Sum of Comments', 0))
            shares = safe_int(row.get('Sum of Shares', 0))
            
            # Validate metrics (must be non-negative)
            views_3sec = max(0, views_3sec)
            views_1min = max(0, views_1min)
            reactions = max(0, reactions)
            comments = max(0, comments)
            shares = max(0, shares)
            
            # Use 3-second views as impressions
            impressions = max(views_3sec, 100)
            reach = int(impressions * 0.75)
            
            # Estimate follower count
            base_followers = 8000
            if not pd.isna(timestamp):
                start_date = pd.Timestamp('2019-01-01')
                days_diff = int((timestamp - start_date).days)
                follower_count = base_followers + (days_diff * 2)
            else:
                follower_count = base_followers
            
            # Ensure follower count is reasonable
            follower_count = max(0, follower_count)
            
            # Determine media type
            if views_1min > 0 or views_3sec > 20:
                media_type = 'Video'
            else:
                media_type = 'Image'
            
            # Extract demographics
            gender = extract_dominant_gender_fb(row)
            age = extract_dominant_age_fb(row)
            location = extract_location_fb(row)
            
            # Generate hashtags
            hashtags = generate_hashtags(media_type, timestamp)
            
            # Create standard record
            record = {
                'post_id': f'fb_post_{idx:04d}',
                'timestamp': timestamp,
                'caption': f'Post from {timestamp.strftime("%B %d, %Y at %I:%M %p")}',
                'likes': reactions,
                'comments': comments,
                'shares': shares,
                'saves': int((reactions + comments + shares) * 0.1),
                'impressions': impressions,
                'reach': reach,
                'follower_count': follower_count,
                'audience_gender': gender,
                'audience_age': age,
                'location': location,
                'hashtags': hashtags,
                'media_type': media_type
            }
            
            standard_data.append(record)
        
        except Exception as e:
            error_count += 1
            if error_count <= 5:  # Only log first 5 errors to avoid spam
                print(f"⚠️ Warning: Error processing Facebook row {idx}: {e}")
            continue
    
    if error_count > 0:
        print(f"⚠️ Encountered {error_count} errors while processing Facebook data. Successfully processed {len(standard_data)} records.")
    
    if len(standard_data) == 0:
        raise ValueError("No valid data could be extracted from the Facebook file")
    
    print(f"✅ Successfully converted {len(standard_data)} Facebook posts to standard format")
    return pd.DataFrame(standard_data)


def safe_int(value, default=0):
    """Safely convert value to integer, handling NaN"""
    try:
        if pd.isna(value) or value == '' or value is None:
            return default
        if isinstance(value, str):
            # Remove commas and other non-numeric characters
            value = ''.join(filter(lambda x: x.isdigit() or x == '.' or x == '-', value))
            if value == '':
                return default
        return int(float(value))
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    """Safely convert value to float, handling NaN"""
    try:
        if pd.isna(value) or value == '' or value is None:
            return default
        if isinstance(value, str):
            # Remove commas and other non-numeric characters
            value = ''.join(filter(lambda x: x.isdigit() or x == '.' or x == '-', value))
            if value == '':
                return default
        return float(value)
    except (ValueError, TypeError):
        return default


def extract_hashtags(text):
    """Extract hashtags from text"""
    if pd.isna(text) or text == '':
        return '#socialmedia #content'
    
    # Find hashtags in text
    hashtags = re.findall(r'#\w+', str(text))
    
    if hashtags:
        return ' '.join(hashtags[:10])  # Limit to 10 hashtags
    else:
        return '#socialmedia #content'


def extract_dominant_gender_fb(row):
    """Extract dominant gender from Facebook analytics"""
    male_cols = [col for col in row.index if '(M,' in str(col)]
    female_cols = [col for col in row.index if '(F,' in str(col)]
    
    male_sum = sum(safe_int(row.get(col, 0)) for col in male_cols)
    female_sum = sum(safe_int(row.get(col, 0)) for col in female_cols)
    
    if male_sum > female_sum * 1.2:
        return 'Male'
    elif female_sum > male_sum * 1.2:
        return 'Female'
    else:
        return 'Mixed'


def extract_dominant_age_fb(row):
    """Extract dominant age group from Facebook analytics"""
    age_groups = {
        '18-24': [],
        '25-34': [],
        '35-44': [],
        '45-54': [],
        '55-64': [],
        '65+': []
    }
    
    for col in row.index:
        col_str = str(col)
        for age in age_groups.keys():
            if age in col_str:
                age_groups[age].append(safe_int(row.get(col, 0)))
    
    age_sums = {age: sum(values) for age, values in age_groups.items()}
    
    if age_sums:
        dominant_age = max(age_sums, key=lambda x: age_sums[x])
        return dominant_age
    
    return '25-34'


def extract_location_fb(row):
    """Extract location from Facebook analytics"""
    location_cols = [col for col in row.index if 'country' in str(col).lower()]
    
    for col in location_cols:
        if 'India' in str(col) or 'IN' in str(col):
            return 'India'
        elif 'US' in str(col) or 'United States' in str(col):
            return 'United States'
    
    return 'India'


def generate_hashtags(media_type, timestamp):
    """Generate relevant hashtags based on media type and date"""
    base_tags = ['#socialmedia', '#digital', '#content']
    
    if media_type == 'Video':
        base_tags.extend(['#video', '#reel', '#viral'])
    elif media_type == 'Carousel':
        base_tags.extend(['#carousel', '#gallery'])
    else:
        base_tags.extend(['#photo', '#instagram'])
    
    # Add month-based tags
    month = timestamp.strftime('%B').lower()
    base_tags.append(f'#{month}')
    
    return ' '.join(base_tags[:8])



def normalize_columns(df):
    """Normalize column names to standard lowercase format"""
    # Create a mapping dictionary
    column_mapping = {}
    for col in df.columns:
        col_clean = str(col).lower().strip().replace(' ', '_').replace('-', '_')
        
        # Map timestamp/date
        if col_clean in ['date', 'time', 'publish_time', 'created_at', 'posted_at', 'timestamp', 'date_posted']:
            column_mapping[col] = 'timestamp'
            
        # Map metrics
        elif col_clean in ['like', 'likes', 'like_count', 'reactions', 'favorites']:
            column_mapping[col] = 'likes'
        elif col_clean in ['comment', 'comments', 'comment_count']:
            column_mapping[col] = 'comments'
        elif col_clean in ['share', 'shares', 'share_count', 'reshares']:
            column_mapping[col] = 'shares'
        elif col_clean in ['view', 'views', 'view_count', 'impressions', 'video_views']:
            column_mapping[col] = 'impressions'
        elif col_clean in ['reach', 'people_reached', 'unique_views']:
            column_mapping[col] = 'reach'
        elif col_clean in ['follower', 'followers', 'follower_count', 'follows', 'subscribers']:
            column_mapping[col] = 'follower_count'
        elif col_clean in ['save', 'saves', 'saved']:
            column_mapping[col] = 'saves'
            
        # Map content
        elif col_clean in ['caption', 'text', 'description', 'message', 'copy', 'content']:
            column_mapping[col] = 'caption'
        elif col_clean in ['type', 'media_type', 'post_type', 'content_type', 'asset_type']:
            column_mapping[col] = 'media_type'
        elif col_clean in ['id', 'post_id', 'postid', 'content_id']:
            column_mapping[col] = 'post_id'
        elif col_clean in ['link', 'permalink', 'url', 'post_link']:
            column_mapping[col] = 'permalink'
        elif col_clean in ['hashtags', 'tags', 'topics']:
            column_mapping[col] = 'hashtags'
            
    # Rename columns
    df = df.rename(columns=column_mapping)
    return df


def find_header_row(file_path):
    """
    Scan the first few rows of the file to find the likely header row.
    Returns the row index (0-based) or 0 if not found.
    """
    try:
        # Read first 15 lines simply as text to avoid pandas header parsing issues
        # Use simple open instead of pandas to be safer/faster for scanning
        with open(file_path, 'r', errors='ignore') as f:
            lines = [f.readline() for _ in range(15)]
            
        keywords = [
            'row labels', 'post id', 'timestamp', 'date', 'permalink', 
            '3-second video views', 'impressions', 'reach', 'engagements'
        ]
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            # If line contains at least 2 key terms matches, it's likely the header
            matches = sum(1 for k in keywords if k in line_lower)
            if matches >= 1:
                # Stronger check: "Row Labels" is very specific to FB
                if 'row labels' in line_lower or 'post id' in line_lower:
                    return i
                # If just date/timestamp, might be data, so be careful. 
                # Usually header has many commas
                if line.count(',') > 3 and matches >= 2:
                    return i
                    
        return 0
    except:
        return 0

def adapt_csv_data(file_path, max_retries=3):
    """
    Main function to adapt any CSV format to standard format with error recovery
    """
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # 1. Detect Header Row
            header_row = find_header_row(file_path)
            
            # Try reading the CSV with detected header
            df = pd.read_csv(file_path, header=header_row, encoding='utf-8')
            
            # 2. Detect format based on correctly loaded columns
            csv_format = detect_csv_format(df)
            
            print(f"Detected format: {csv_format} (Header at row {header_row})")
            
            # 3. Convert based on format
            if csv_format == 'instagram_post_export':
                return clean_instagram_post_export(df)
            elif csv_format == 'facebook_video_export':
                # Clean function might need adjustment as it assumes header might be wrong, 
                # but we fixed header loading. Let's rely on column names.
                return clean_facebook_video_export(df)
            else:
                # For standard or unknown, try to normalize
                df = normalize_columns(df)
                
                # Ensure timestamp is datetime
                if 'timestamp' in df.columns:
                    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                
                # Ensure post_id exists
                if 'post_id' not in df.columns:
                    df['post_id'] = [f'post_{i}' for i in range(len(df))]
                    
                # Ensure numeric columns are numeric
                numeric_cols = ['likes', 'comments', 'shares', 'impressions', 'reach', 'follower_count', 'saves']
                for col in numeric_cols:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                        
                return df
                
        except UnicodeDecodeError as e:
            retry_count += 1
            if retry_count < max_retries:
                print(f"⚠️ Unicode decode error (attempt {retry_count}), trying different encoding...")
                try:
                    df = pd.read_csv(file_path, header=find_header_row(file_path), encoding='latin-1')
                    continue  # Retry with the new dataframe
                except:
                    pass
            else:
                # Try Excel as last resort
                try:
                    df = pd.read_excel(file_path, header=find_header_row(file_path))
                    continue  # Retry with the new dataframe
                except Exception as excel_error:
                    raise ValueError(f"Could not read file after {max_retries} attempts: {excel_error}")
        except Exception as e:
            retry_count += 1
            if retry_count < max_retries:
                print(f"⚠️ Error reading file (attempt {retry_count}), retrying...")
                import time
                time.sleep(2 ** retry_count)  # Exponential backoff
            else:
                raise ValueError(f"Could not read file after {max_retries} attempts: {e}")
    
    # This should never be reached
    raise ValueError("Unexpected execution path in adapt_csv_data")


def adapt_csv_data_chunk(df_chunk):
    """
    Process a chunk of data for large file handling
    """
    # Detect format based on chunk columns
    csv_format = detect_csv_format(df_chunk)
    
    # Convert based on format
    if csv_format == 'instagram_post_export':
        return clean_instagram_post_export(df_chunk)
    elif csv_format == 'facebook_video_export':
        return clean_facebook_video_export(df_chunk)
    else:
        # For standard or unknown, try to normalize
        df_chunk = normalize_columns(df_chunk)
        
        # Ensure timestamp is datetime
        if 'timestamp' in df_chunk.columns:
            df_chunk['timestamp'] = pd.to_datetime(df_chunk['timestamp'], errors='coerce')
        
        # Ensure post_id exists
        if 'post_id' not in df_chunk.columns:
            df_chunk['post_id'] = [f'post_{i}' for i in range(len(df_chunk))]
            
        # Ensure numeric columns are numeric
        numeric_cols = ['likes', 'comments', 'shares', 'impressions', 'reach', 'follower_count', 'saves']
        for col in numeric_cols:
            if col in df_chunk.columns:
                df_chunk[col] = pd.to_numeric(df_chunk[col], errors='coerce').fillna(0)
                
        return df_chunk


if __name__ == "__main__":
    # Test the adapter
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        result = adapt_csv_data(file_path)
        print(f"\nSuccessfully converted {len(result)} records")
        print(f"\nColumns: {list(result.columns)}")
        print(f"\nFirst few rows:\n{result.head()}")

