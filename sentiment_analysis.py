"""
Comprehensive Sentiment Analysis Module
Advanced NLP for social media content analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Try importing NLP libraries
try:
    from textblob import TextBlob
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False


def analyze_sentiment(text):
    """Analyze sentiment with polarity and subjectivity"""
    if pd.isna(text) or text == '':
        return {'sentiment': 'Neutral', 'polarity': 0.0, 'subjectivity': 0.0, 'emotion': '😐 Neutral'}
    
    try:
        blob = TextBlob(str(text))
        # Access sentiment attributes directly to avoid type checking issues
        polarity = float(blob.sentiment.polarity)
        subjectivity = float(blob.sentiment.subjectivity)
        
        # Determine sentiment
        if polarity > 0.1:
            sentiment = 'Positive'
        elif polarity < -0.1:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        # Determine emotion based on polarity and subjectivity
        if polarity > 0.6:
            emotion = '😍 Joy'
        elif polarity > 0.3:
            emotion = '😊 Happy'
        elif polarity < -0.6:
            emotion = '😡 Anger'
        elif polarity < -0.3:
            emotion = '😢 Sad'
        elif subjectivity > 0.7:
            emotion = '😲 Surprise'
        elif polarity > 0:
            emotion = '😌 Content'
        else:
            emotion = '😐 Neutral'
        
        return {
            'sentiment': sentiment,
            'polarity': polarity,
            'subjectivity': subjectivity,
            'emotion': emotion
        }
    except:
        return {'sentiment': 'Neutral', 'polarity': 0.0, 'subjectivity': 0.0, 'emotion': '😐 Neutral'}



@st.cache_data(show_spinner=False)
def process_sentiment_for_dataframe(df_dict, text_column):
    """
    Cached sentiment processing.
    Accepts specific columns as dict/df to ensure cache stability.
    Returns processed dataframe with sentiment columns.
    """
    # Reconstruct dataframe from input
    data = pd.DataFrame(df_dict)
    
    # Pre-calculate lists for speed
    sentiments_list = []
    
    # Helper for single text analysis (inline for speed within cached function)
    def _get_sentiment(text):
        if pd.isna(text) or text == '':
            return 'Neutral', 0.0, 0.0, '😐 Neutral'
        try:
            blob = TextBlob(str(text))
            p = float(blob.sentiment.polarity)
            s = float(blob.sentiment.subjectivity)
            
            # Sentiment
            if p > 0.1: sent = 'Positive'
            elif p < -0.1: sent = 'Negative'
            else: sent = 'Neutral'
            
            # Emotion
            if p > 0.6: emo = '😍 Joy'
            elif p > 0.3: emo = '😊 Happy'
            elif p < -0.6: emo = '😡 Anger'
            elif p < -0.3: emo = '😢 Sad'
            elif s > 0.7: emo = '😲 Surprise'
            elif p > 0: emo = '😌 Content'
            else: emo = '😐 Neutral'
            
            return sent, p, s, emo
        except:
             return 'Neutral', 0.0, 0.0, '😐 Neutral'

    # Batch process
    texts = data[text_column].tolist()
    results = [_get_sentiment(t) for t in texts]
    
    # Assign back
    data['sentiment'] = [r[0] for r in results]
    data['polarity'] = [r[1] for r in results]
    data['subjectivity'] = [r[2] for r in results]
    data['emotion'] = [r[3] for r in results]
    
    return data

def render_sentiment_analysis(data):
    """Main sentiment analysis dashboard"""
    
    if not NLP_AVAILABLE:
        st.error("❌ TextBlob not installed.")
        st.code("pip install textblob", language="bash")
        return
    
    # Header
    from professional_dashboard import render_professional_header
    render_professional_header("💬 Sentiment Analysis", "AI-powered emotion detection and sentiment insights")

    
    # Check for caption column
    text_column = None
    possible_cols = ['caption', 'text', 'content', 'message', 'description']
    for col in possible_cols:
        if col in data.columns:
            text_column = col
            break
    
    if text_column is None:
        st.warning("⚠️ No text/caption data found.")
        return
    
    st.success(f"✅ Analyzing text from column: **{text_column}**")
    
    # Analyze all captions (Cached)
    with st.spinner('🔍 Analyzing sentiment (cached)...'):
        # Pass only necessary column and ID to cache effectively
        # We need a unique identifier (like index) to merge back if needed, 
        # but here we just process the text column and return a DF aligned with it.
        # To be safe, we pass the subset of data we need.
        input_data = data[[text_column]].copy()
        
        # We convert to dict for caching optimization if DF is huge, but DF is usually fine.
        # The function expects a dict or DF. Let's pass the DF directly but ensure specific columns.
        processed_data = process_sentiment_for_dataframe(input_data, text_column)
        
        # Merge results back to main data for visualization (this part is fast)
        data['sentiment'] = processed_data['sentiment']
        data['polarity'] = processed_data['polarity']
        data['subjectivity'] = processed_data['subjectivity']
        data['emotion'] = processed_data['emotion']
    
    # Summary Metrics
    st.markdown("### 📊 Sentiment Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        positive_pct = (data['sentiment'] == 'Positive').sum() / len(data) * 100
        st.metric("Positive Posts", f"{positive_pct:.1f}%", "🟢")
    
    with col2:
        negative_pct = (data['sentiment'] == 'Negative').sum() / len(data) * 100
        st.metric("Negative Posts", f"{negative_pct:.1f}%", "🔴")
    
    with col3:
        avg_polarity = data['polarity'].mean()
        st.metric("Avg Polarity", f"{avg_polarity:.2f}", "📈")
    
    with col4:
        avg_subjectivity = data['subjectivity'].mean()
        st.metric("Avg Subjectivity", f"{avg_subjectivity:.2f}", "📊")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 1: Sentiment Distribution & Emotion Breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        # Matplotlib Sentiment Distribution
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', 
               colors=[colors.get(s, '#94a3b8') for s in sentiment_counts.index], wedgeprops={'width': 0.4})
        ax.set_title('Sentiment Distribution')
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Matplotlib Emotion Breakdown
        fig, ax = plt.subplots(figsize=(8, 5))
        y_pos = np.arange(len(emotion_counts))
        ax.barh(y_pos, emotion_counts.values, color=[emotion_colors.get(e, '#94a3b8') for e in emotion_counts.index])
        ax.set_yticks(y_pos)
        ax.set_yticklabels(emotion_counts.index)
        ax.invert_yaxis()
        ax.set_xlabel('Post Count')
        ax.set_title('Emotion Breakdown')
        sns.despine()
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Sentiment vs Engagement & Polarity Timeline
    col3, col4 = st.columns(2)
    
    with col3:
        # Matplotlib Sentiment vs Engagement
        fig, ax = plt.subplots(figsize=(8, 5))
        x = np.arange(len(sentiment_engagement))
        width = 0.25
        
        ax.bar(x - width, sentiment_engagement['likes'], width, label='Likes', color='#667eea')
        if 'comments' in sentiment_engagement.columns:
            ax.bar(x, sentiment_engagement['comments'], width, label='Comments', color='#f093fb')
        if 'shares' in sentiment_engagement.columns:
            ax.bar(x + width, sentiment_engagement['shares'], width, label='Shares', color='#10b981')
            
        ax.set_xticks(x)
        ax.set_xticklabels(sentiment_engagement.index)
        ax.set_ylabel('Average Count')
        ax.set_title('Sentiment vs Engagement')
        ax.legend()
        sns.despine()
        st.pyplot(fig)
        
        best_sentiment = sentiment_engagement['likes'].idxmax()
        best_likes = sentiment_engagement['likes'].max()
        st.markdown(f"💡 **{best_sentiment} posts** perform best with {best_likes:.0f} avg likes")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        # Matplotlib Polarity Over Time
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(daily_polarity.index, daily_polarity['polarity'], color='#667eea', linewidth=3)
        ax.fill_between(daily_polarity.index, daily_polarity['polarity'], color='#667eea', alpha=0.2)
        ax.axhline(0, color='#94a3b8', linestyle='--')
        ax.set_ylabel('Polarity Score')
        ax.set_ylim(-1.1, 1.1)
        ax.set_title('Polarity Over Time')
        plt.xticks(rotation=45)
        sns.despine()
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 3: Hashtag Sentiment & Word Analysis
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown('<div class="pro-glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">🏷️ Top Hashtags by Sentiment</div>', unsafe_allow_html=True)
        
        if 'hashtags' in data.columns:
            hashtag_data = []
            for idx, row in data.iterrows():
                if pd.notna(row['hashtags']):
                    tags = str(row['hashtags']).split(',')
                    for tag in tags[:5]:
                        tag = tag.strip()
                        if tag:
                            hashtag_data.append({
                                'hashtag': tag,
                                'sentiment': row['sentiment'],
                                'polarity': row['polarity'],
                                'likes': row.get('likes', 0)
                            })
            
            if hashtag_data:
                ht_df = pd.DataFrame(hashtag_data)
                top_hashtags = ht_df.groupby(['hashtag', 'sentiment']).size().unstack(fill_value=0)
                top_hashtags['total'] = top_hashtags.sum(axis=1)
                top_hashtags = top_hashtags.nlargest(10, 'total')
                
                # Matplotlib Hashtag Sentiment
                fig, ax = plt.subplots(figsize=(8, 6))
                top_hashtags[['Positive', 'Neutral', 'Negative']].plot(kind='bar', stacked=True, 
                                                                    color=['#10b981', '#f59e0b', '#ef4444'], ax=ax)
                ax.set_title('Top Hashtags by Sentiment')
                ax.set_ylabel('Post Count')
                plt.xticks(rotation=45)
                sns.despine()
                st.pyplot(fig)
            else:
                st.info("No hashtag data available")
        else:
            st.info("No hashtag column found")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col6:
        st.markdown('<div class="pro-glass-card fade-in">', unsafe_allow_html=True)
        st.markdown('<div class="pro-chart-title">📝 Caption Length vs Sentiment</div>', unsafe_allow_html=True)
        
        data['caption_length'] = data[text_column].astype(str).str.len()
        
        # Matplotlib Caption Length vs Sentiment
        fig, ax = plt.subplots(figsize=(8, 5))
        for sentiment in ['Positive', 'Neutral', 'Negative']:
            subset = data[data['sentiment'] == sentiment]
            ax.scatter(subset['caption_length'], subset['polarity'], label=sentiment, alpha=0.6, color=colors.get(sentiment, '#94a3b8'))
        
        ax.set_xlabel('Caption Length (chars)')
        ax.set_ylabel('Polarity Score')
        ax.set_title('Caption Length vs Sentiment')
        ax.legend()
        sns.despine()
        st.pyplot(fig)
        
        avg_length_by_sentiment = data.groupby('sentiment')['caption_length'].mean()
        optimal_sentiment = avg_length_by_sentiment.idxmax()
        st.markdown(f"💡 **{optimal_sentiment}** posts avg {avg_length_by_sentiment[optimal_sentiment]:.0f} characters")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Emotion Timeline
    st.markdown('<div class="pro-glass-card fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="pro-chart-title">🎭 Emotion Timeline</div>', unsafe_allow_html=True)
    
    if 'timestamp' in data.columns:
        emotion_timeline = data.groupby([pd.Grouper(key='timestamp', freq='D'), 'emotion']).size().reset_index(name='count')
        
        # Matplotlib Emotion Timeline (Simplified area chart)
        fig, ax = plt.subplots(figsize=(10, 5))
        pivoted_emotions = emotion_timeline.pivot(index='timestamp', columns='emotion', values='count').fillna(0)
        pivoted_emotions.plot.area(ax=ax, color=[emotion_colors.get(c, '#94a3b8') for c in pivoted_emotions.columns], alpha=0.6)
        
        ax.set_title('Emotion Timeline')
        ax.set_ylabel('Post Count')
        plt.xticks(rotation=45)
        sns.despine()
        st.pyplot(fig)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Top Posts by Sentiment
    st.markdown('<div class="pro-glass-card fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="pro-chart-title">🏆 Top Performing Posts by Sentiment</div>', unsafe_allow_html=True)
    
    sentiment_tabs = st.tabs(['Positive 😊', 'Neutral 😐', 'Negative 😢'])
    
    for idx, (sentiment_name, tab) in enumerate(zip(['Positive', 'Neutral', 'Negative'], sentiment_tabs)):
        with tab:
            sentiment_posts = data[data['sentiment'] == sentiment_name]
            if len(sentiment_posts) > 0 and 'likes' in sentiment_posts.columns:
                top_posts = sentiment_posts.nlargest(5, 'likes')[['timestamp', 'caption', 'likes', 'emotion', 'polarity']]
                top_posts['caption'] = top_posts['caption'].str[:80] + '...'
                st.dataframe(top_posts, use_container_width=True, hide_index=True)
            else:
                st.info(f"No {sentiment_name.lower()} posts found")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Insights
    st.markdown('<div class="pro-insights fade-in">', unsafe_allow_html=True)
    st.markdown('### 💡 AI-Powered Sentiment Insights')
    
    # Calculate insights
    dominant_sentiment = data['sentiment'].mode()[0] if len(data['sentiment'].mode()) > 0 else 'Neutral'
    dominant_emotion = data['emotion'].mode()[0] if len(data['emotion'].mode()) > 0 else '😐 Neutral'
    
    # Initialize variables to avoid unbound errors
    best_performing_sentiment = 'Neutral'
    sentiment_lift = 0.0
    
    if 'likes' in data.columns:
        best_performing_sentiment = data.groupby('sentiment')['likes'].mean().idxmax()
        sentiment_lift = ((data[data['sentiment'] == best_performing_sentiment]['likes'].mean() / 
                          data['likes'].mean() - 1) * 100)
    
    st.markdown(f'<div class="pro-insight-item">📊 <strong>Dominant Sentiment:</strong> {dominant_sentiment} ({(data["sentiment"]==dominant_sentiment).sum()}/{len(data)} posts, {(data["sentiment"]==dominant_sentiment).sum()/len(data)*100:.1f}%)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pro-insight-item">🎭 <strong>Most Common Emotion:</strong> {dominant_emotion}</div>', unsafe_allow_html=True)
    
    if 'likes' in data.columns:
        st.markdown(f'<div class="pro-insight-item">🚀 <strong>Best Performing:</strong> {best_performing_sentiment} posts get {sentiment_lift:+.1f}% more engagement</div>', unsafe_allow_html=True)
    
    avg_polarity = data['polarity'].mean()
    if avg_polarity > 0.2:
        st.markdown('<div class="pro-insight-item">✅ <strong>Overall Tone:</strong> Your content has a positive tone! Keep it up!</div>', unsafe_allow_html=True)
    elif avg_polarity < -0.2:
        st.markdown('<div class="pro-insight-item">⚠️ <strong>Overall Tone:</strong> Content leans negative. Consider more uplifting messages.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="pro-insight-item">ℹ️ <strong>Overall Tone:</strong> Balanced neutral tone. Mix in more emotional content for engagement.</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)