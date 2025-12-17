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
    """Convert Instagram post-level export to standard format"""
    
    standard_data = []
    
    for idx, row in df.iterrows():
        try:
            # Extract post ID
            post_id = str(row.get('Post ID', f'post_{idx:04d}'))
            
            # Parse timestamp
            timestamp_str = str(row.get('Publish time', ''))
            try:
                timestamp = pd.to_datetime(timestamp_str, format='%m/%d/%Y %H:%M', errors='coerce')
                if pd.isna(timestamp):
                    timestamp = pd.to_datetime(timestamp_str, errors='coerce')
            except:
                timestamp = pd.Timestamp.now()
            
            if pd.isna(timestamp):
                continue
            
            # Extract metrics
            views = safe_int(row.get('Views', 0))
            reach = safe_int(row.get('Reach', 0))
            likes = safe_int(row.get('Likes', 0))
            comments = safe_int(row.get('Comments', 0))
            shares = safe_int(row.get('Shares', 0))
            follows = safe_int(row.get('Follows', 0))
            saves = safe_int(row.get('Saves', 0))
            
            # Use Views as impressions if available
            impressions = views if views > 0 else reach
            if impressions == 0:
                impressions = max(likes * 10, 100)
            
            # Ensure reach is reasonable
            if reach == 0:
                reach = int(impressions * 0.75)
            
            # Extract description/caption
            caption = str(row.get('Description', ''))[:200]
            
            # Determine media type
            post_type = str(row.get('Post type', 'IG image')).lower()
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
            
            # Demographics - default values
            gender = 'Mixed'
            age = '18-24'
            location = 'India'
            
            # Create standard record
            record = {
                'post_id': post_id,
                'timestamp': timestamp,
                'caption': caption if caption != 'nan' else f'Post from {timestamp.strftime("%B %d, %Y")}',
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
            print(f"Error processing row {idx}: {e}")
            continue
    
    if len(standard_data) == 0:
        raise ValueError("No valid data could be extracted from the file")
    
    return pd.DataFrame(standard_data)


def clean_facebook_video_export(df):
    """Convert Facebook video analytics export to standard format"""
    
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
    
    # Get the date column (first column)
    date_col = df.columns[0]
    
    standard_data = []
    
    for idx, row in df.iterrows():
        try:
            # Extract date/timestamp
            date_str = str(row[date_col]).strip()
            if date_str == 'nan' or date_str == '':
                continue
            
            # Parse date
            try:
                timestamp = pd.to_datetime(date_str, errors='coerce')
            except:
                continue
            
            if pd.isna(timestamp):
                continue
            
            # Extract metrics
            views_3sec = safe_int(row.get('Sum of 3-second video views', 0))
            views_1min = safe_int(row.get('Sum of 1-minute video views', 0))
            reactions = safe_int(row.get('Sum of Reactions', 0))
            comments = safe_int(row.get('Sum of Comments', 0))
            shares = safe_int(row.get('Sum of Shares', 0))
            
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
            print(f"Error processing row {idx}: {e}")
            continue
    
    if len(standard_data) == 0:
        raise ValueError("No valid data could be extracted from the file")
    
    return pd.DataFrame(standard_data)


def safe_int(value):
    """Safely convert value to integer"""
    try:
        if pd.isna(value) or value == '':
            return 0
        return int(float(value))
    except:
        return 0


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


def adapt_csv_data(file_path):
    """
    Main function to adapt any CSV format to standard format
    """
    try:
        # Try reading the CSV
        df = pd.read_csv(file_path, encoding='utf-8')
    except:
        try:
            df = pd.read_csv(file_path, encoding='latin-1')
        except Exception as e:
            raise ValueError(f"Could not read CSV file: {e}")
    
    # Detect format
    csv_format = detect_csv_format(df)
    
    print(f"Detected format: {csv_format}")
    
    # Convert based on format
    if csv_format == 'instagram_post_export':
        return clean_instagram_post_export(df)
    elif csv_format == 'facebook_video_export':
        return clean_facebook_video_export(df)
    elif csv_format == 'standard':
        return df
    else:
        raise ValueError(f"Unknown CSV format. Please check your file structure.")


if __name__ == "__main__":
    # Test the adapter
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        result = adapt_csv_data(file_path)
        print(f"\nSuccessfully converted {len(result)} records")
        print(f"\nColumns: {list(result.columns)}")
        print(f"\nFirst few rows:\n{result.head()}")
