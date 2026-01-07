import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

@pytest.fixture
def mock_social_data():
    """Provides a sample dataframe for analytics testing"""
    data = {
        'post_id': ['post1', 'post2', 'post3'],
        'timestamp': [
            datetime.now() - timedelta(days=2),
            datetime.now() - timedelta(days=1),
            datetime.now()
        ],
        'caption': ['Hello world #testing', 'Another post #analytics', 'Final post #results'],
        'likes': [100, 200, 150],
        'comments': [10, 20, 15],
        'shares': [5, 10, 8],
        'saves': [2, 4, 3],
        'impressions': [1000, 2000, 1500],
        'reach': [800, 1600, 1200],
        'follower_count': [1000, 1000, 1000],
        'audience_gender': ['Mixed', 'Female', 'Male'],
        'audience_age': ['18-24', '18-24', '18-24'],
        'location': ['Delhi', 'Mumbai', 'Bangalore'],
        'hashtags': ['#testing', '#analytics', '#results'],
        'media_type': ['Image', 'Video', 'Image']
    }
    return pd.DataFrame(data)

@pytest.fixture
def temp_db(tmp_path):
    """Provides a temporary database path for isolation"""
    db_path = tmp_path / "test_social_media.db"
    return str(db_path)
