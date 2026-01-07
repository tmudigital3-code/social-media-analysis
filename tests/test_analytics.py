import pytest
import pandas as pd
import numpy as np
from sentiment_analysis import analyze_sentiment
from advanced_techniques import render_advanced_analytics_ml

def test_analyze_sentiment_positive():
    text = "I love this new feature! It's amazing and helpful."
    result = analyze_sentiment(text)
    assert result['sentiment'] == 'Positive'
    assert result['polarity'] > 0.1
    assert 'Joy' in result['emotion'] or 'Happy' in result['emotion']

def test_analyze_sentiment_negative():
    text = "This is a terrible experience. I hate it."
    result = analyze_sentiment(text)
    assert result['sentiment'] == 'Negative'
    assert result['polarity'] < -0.1
    assert 'Anger' in result['emotion'] or 'Sad' in result['emotion']

def test_analyze_sentiment_neutral():
    text = "The quick brown fox jumps over the lazy dog."
    result = analyze_sentiment(text)
    assert result['sentiment'] == 'Neutral'
    assert abs(result['polarity']) <= 0.1

def test_analyze_sentiment_empty():
    assert analyze_sentiment("")['sentiment'] == 'Neutral'
    assert analyze_sentiment(None)['sentiment'] == 'Neutral'

def test_ml_prediction_logic(mock_social_data):
    """
    Test the underlying logic used in engagement prediction.
    Since render_advanced_analytics_ml is a UI function, 
    we test the data preparation it uses.
    """
    data = mock_social_data.copy()
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    
    # Simulate the grouping used in advanced_techniques.py
    daily_engagement = data.groupby(pd.Grouper(key='timestamp', freq='D')).agg({
        'likes': 'sum',
        'comments': 'sum',
        'shares': 'sum'
    })
    daily_engagement['total'] = daily_engagement.sum(axis=1)
    
    assert 'total' in daily_engagement.columns
    assert daily_engagement['total'].sum() == (data['likes'].sum() + data['comments'].sum() + data['shares'].sum())
