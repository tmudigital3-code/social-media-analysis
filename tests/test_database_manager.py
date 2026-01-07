import pytest
import pandas as pd
import os
import sqlite3
import database_manager

@pytest.fixture
def mock_db(tmp_path, monkeypatch):
    """Isolate DB operations to a temporary file"""
    db_file = tmp_path / "test_social.db"
    monkeypatch.setattr(database_manager, "DB_FILE", str(db_file))
    database_manager.init_db()
    return str(db_file)

def test_init_db(mock_db):
    """Verify that database and table are created"""
    assert os.path.exists(mock_db)
    conn = sqlite3.connect(mock_db)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='posts'")
    assert c.fetchone() is not None
    conn.close()

def test_save_and_load_data(mock_db, mock_social_data):
    """Verify saving and loading from the database"""
    database_manager.save_data(mock_social_data)
    loaded_df = database_manager.load_data()
    
    # Check that data was saved and loaded correctly
    assert len(loaded_df) == len(mock_social_data)
    assert 'post_id' in loaded_df.columns
    assert loaded_df.iloc[0]['post_id'] == 'post1'
    # Check that numeric conversion worked
    assert loaded_df.iloc[0]['likes'] == 100

def test_save_empty_df(mock_db):
    """Verify that saving an empty dataframe doesn't crash and handles it gracefully"""
    empty_df = pd.DataFrame()
    database_manager.save_data(empty_df)
    loaded_df = database_manager.load_data()
    assert loaded_df.empty

def test_deduplication(mock_db, mock_social_data):
    """Verify that duplicate post_ids are handled (updated or ignored)"""
    database_manager.save_data(mock_social_data)
    
    # Create a duplicate with updated metrics
    duplicate_data = mock_social_data.iloc[[0]].copy()
    duplicate_data.at[0, 'likes'] = 999
    
    database_manager.save_data(duplicate_data)
    loaded_df = database_manager.load_data()
    
    # Should still have 3 records, but first one should have 999 likes (due to delete/reinsert logic in save_data)
    assert len(loaded_df) == 3
    updated_record = loaded_df[loaded_df['post_id'] == 'post1']
    assert updated_record.iloc[0]['likes'] == 999
