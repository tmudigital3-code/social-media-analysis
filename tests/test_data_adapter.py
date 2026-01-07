import pytest
import pandas as pd
import numpy as np
from data_adapter import detect_csv_format, normalize_columns, clean_instagram_post_export, adapt_csv_data

def test_detect_csv_format():
    # Instagram format
    ig_df = pd.DataFrame(columns=['Post ID', 'Account Username', 'Description'])
    assert detect_csv_format(ig_df) == 'instagram_post_export'
    
    # Facebook format
    fb_df = pd.DataFrame(columns=['Title', '3-second video views', 'Sum of Reactions'])
    assert detect_csv_format(fb_df) == 'facebook_video_export'
    
    # Standard format
    std_df = pd.DataFrame(columns=['post_id', 'timestamp', 'likes'])
    assert detect_csv_format(std_df) == 'standard'
    
    # Unknown format
    unk_df = pd.DataFrame(columns=['Random', 'Column'])
    assert detect_csv_format(unk_df) == 'unknown'

def test_normalize_columns():
    df = pd.DataFrame(columns=['Like', 'Comment Count', 'Content', 'Posted At'])
    normalized_df = normalize_columns(df)
    
    assert 'likes' in normalized_df.columns
    assert 'comments' in normalized_df.columns
    assert 'caption' in normalized_df.columns
    assert 'timestamp' in normalized_df.columns

def test_clean_instagram_post_export():
    ig_data = {
        'Post ID': ['ig1'],
        'Publish time': ['01/01/2024 10:00'],
        'Views': [1000],
        'Likes': [100],
        'Description': 'Check this out #cool #insta',
        'Post type': 'IG image'
    }
    ig_df = pd.DataFrame(ig_data)
    cleaned_df = clean_instagram_post_export(ig_df)
    
    assert len(cleaned_df) == 1
    assert cleaned_df.iloc[0]['post_id'] == 'ig1'
    assert cleaned_df.iloc[0]['likes'] == 100
    assert '#cool' in cleaned_df.iloc[0]['hashtags']
    assert cleaned_df.iloc[0]['media_type'] == 'Image'

def test_adapt_csv_data_standard(tmp_path):
    # Create a standard CSV
    csv_file = tmp_path / "std_posts.csv"
    std_data = pd.DataFrame({
        'post_id': ['s1'],
        'timestamp': ['2024-01-01'],
        'likes': [50],
        'comments': [5]
    })
    std_data.to_csv(csv_file, index=False)
    
    result_df = adapt_csv_data(str(csv_file))
    assert len(result_df) == 1
    assert result_df.iloc[0]['likes'] == 50
    assert result_df.iloc[0]['post_id'] == 's1'
